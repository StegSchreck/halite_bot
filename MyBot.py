import hlt
# Then let's import the logging module so we can print out information
import logging


def perform_turn():
    game_map = game.update_map()
    command_queue = []
    planet_queue = []
    my_ships = game_map.get_me().all_ships()
    for ship in my_ships:
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            continue

        sorted_planets = get_planets_sorted_by_distance_for_ship(game_map, ship)
        for planet in sorted_planets:
            if planet.is_owned() or planet in planet_queue:
                continue

            move_ship_to_planet(command_queue, game_map, planet, planet_queue, ship)
            break
    game.send_command_queue(command_queue)


def move_ship_to_planet(command_queue, game_map, planet, planet_queue, ship):
    if ship.can_dock(planet):
        command_queue.append(ship.dock(planet))
    else:
        navigate_command = ship.navigate(
            ship.closest_point_to(planet),
            game_map,
            speed=int(hlt.constants.MAX_SPEED)
        )
        planet_queue.append(planet_queue)
        if navigate_command:
            command_queue.append(navigate_command)


def get_planets_sorted_by_distance_for_ship(game_map, ship):
    return sorted(game_map.all_planets(), key=lambda p: p.calculate_distance_between(ship))


if __name__ == "__main__":
    # GAME INIT
    game = hlt.Game("StegSchreck")
    logging.info("Starting my Settler bot!")

    # GAME LOOP
    while True:
        perform_turn()
