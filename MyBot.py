import hlt
# Then let's import the logging module so we can print out information
import logging


def perform_turn():
    game_map = game.update_map()
    command_queue = []
    planet_conquer_queue = []
    ship_attack_queue = []
    my_ships = game_map.get_me().all_ships()
    for ship in my_ships:
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            continue

        planets_by_distance = get_planets_sorted_by_distance_for_ship(game_map, ship)
        for planet in planets_by_distance:
            if all_planets_are_owned(game_map):
                enemy_planets_by_distance = [
                    planet for planet in planets_by_distance if planet.owner != game_map.get_me()
                ]
                if len(enemy_planets_by_distance) > 0:
                    enqueue_attack_of_docked_ships(command_queue, game_map, planet, ship_attack_queue, ship)
                    break

            if planet.is_owned() or planet in planet_conquer_queue:
                continue

            enqueue_move_command_for_ship_to_planet(command_queue, game_map, planet, planet_conquer_queue, ship)
            break
    game.send_command_queue(command_queue)


def enqueue_move_command_for_ship_to_planet(command_queue, game_map, planet, planet_conquer_queue, ship):
    if ship.can_dock(planet):
        command_queue.append(ship.dock(planet))
    else:
        navigate_command = ship.navigate(
            ship.closest_point_to(planet),
            game_map,
            speed=int(hlt.constants.MAX_SPEED)
        )
        planet_conquer_queue.append(planet)
        if navigate_command:
            command_queue.append(navigate_command)


def get_planets_sorted_by_distance_for_ship(game_map, ship):
    return sorted(game_map.all_planets(), key=lambda p: p.calculate_distance_between(ship))


def all_planets_are_owned(game_map):
    for planet in game_map.all_planets():
        if not planet.is_owned():
            return False
    return True


def enqueue_attack_of_docked_ships(command_queue, game_map, planet, ship_attack_queue, ship):
    all_docked_enemy_ships = [ship for ship in planet.all_docked_ships() if ship.owner != game_map.get_me()]
    for enemy_ship in all_docked_enemy_ships:
        if enemy_ship not in ship_attack_queue:
            navigate_command = ship.navigate(
                ship.closest_point_to(enemy_ship, 0),
                game_map,
                speed=int(hlt.constants.MAX_SPEED)
            )
            ship_attack_queue.append(enemy_ship)
            if navigate_command:
                command_queue.append(navigate_command)
            break


if __name__ == "__main__":
    # GAME INIT
    game = hlt.Game("StegSchreck")
    logging.info("Starting my Settler bot!")

    # GAME LOOP
    while True:
        perform_turn()
