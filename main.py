from typing import List

import pygame
import matplotlib.pyplot as plt

from src.planet import get_planets, Planet, WIDTH, HEIGHT, time_at_certain_angles

import math
import numpy as np 

def task1():
    """
    Using Solar System parameters, verify
    that the square of orbital period is proportional to the
    cube of the orbital semi-major axis. If units of years
    for time and Astronomical Units (AU) for distance are used, show that the constant of proportionality is very close to unity for the Solar System.
    """
    planets: List[Planet] = get_planets()

    semi_major_axis_three_over_two = []
    orbital_periods = []
    for planet in planets:
        semi_major_axis_three_over_two.append(planet.semi_major_axis ** (3/2))
        orbital_periods.append(planet.orbital_period)
    
    plt.title("Kepler's Third Law")
    plt.xlabel('(a / AU) * (3/2)')
    plt.ylabel('T /Yr')
    plt.plot(semi_major_axis_three_over_two,orbital_periods)
    plt.scatter(semi_major_axis_three_over_two,orbital_periods, 10, 'Red')
    plt.show()


def task2():
    """
    Compute and accurately plot elliptical orbits of the five inner planets.
    Then (using a larger scale), plot the outer planet orbits.
    """
    planets: List[Planet] = get_planets()
    planets = planets[4:]
    for planet in planets:
        planet.create_orbit()
    plt.show()


def task3():
    """
    Create a 2D animation of the orbits of the planets.
    """
    planets: List[Planet] = get_planets()

    pygame.init()
    WIN = pygame.display.set_mode((WIDTH,HEIGHT))
    run = True
    clock = pygame.time.Clock()

    frames = 0

    planets = planets[:4]

    outer_line_coordinates, outer_locations = planets[-1].create_orbit()

    while run and frames < planets[-1].ten_rotations_frames_time():
        clock.tick(60)
        WIN.fill((0,0,0))
        # pygame.display.update()
        frames += 1 #increases by one every frame, counting them

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            togethercoords, locations = planet.create_orbit()
            #locations = planet.increase_locations(planets[-1])
            planet.DRAW(WIN, locations[frames])
            if frames > len(outer_locations) / 60 and run:
                print ("Program closed as a rotation of the outer planet happened")
                run = False
            pygame.draw.lines(WIN, planet.color, False, togethercoords, 2)

        pygame.display.update()
        # WIN.fill((0,0,0))

    pygame.quit()


def task4():
    """
    Use the inclination angle value  and hence plot 3D orbit animations of the planets.
    Do include the dwarf planet Pluto, as it is off the plane of the ecliptic much more than the other planets.
    """
    planets: List[Planet] = get_planets()
    #planets = planets[:4]

    plt.close()
    plt.axes(projection='3d')

    for planet in planets:
        planet.create_orbit_z()
    plt.show()


def task5():
    """
    Use Simpson’s numeric integration method to determine how orbital time varies with polar angle.
    Hence code-up a function which outputs orbit polar angle from orbit time.
    Update your models with this function, and contrast how polar angle varies with time for Pluto,
    compared to a circular motion example with the same 248.348 year period.
    """

    '''initialising values'''
    conversion =  180 / 360 / math.pi
    p = 248.348
    x_values_time = []
    y_values_angle = []
    d_theta = h = 1/1000

    '''THIS IS WHAT COMES BEFORE THE INTEGRAL'''
    constant_times_integral = p * (1 - 0.25**2) ** (3/2) * (1 / (2*math.pi))

    '''creating the values for the circular line'''
    for i in np.arange (0,6 * math.pi):
        x_values_time.append(p * i / math.pi * 180 / 360) 
        y_values_angle.append(i)

    x_values_time.append(time_at_certain_angles((0, round(6 * math.pi,3)), h, "1 / (1 - 0.25 * math.cos(x)) ** 2", 'x') * constant_times_integral) 
    y_values_angle.append(round(6 * math.pi,3))

    '''plotting the blue line'''
    plt.plot(x_values_time,y_values_angle)
    plt.xlabel("time /years")
    plt.ylabel("orbit polar angle /rad")

    '''getting an equally spaced list of angles using numpy.linspace (he did this in his code so idk)'''
    #number_orbits = int(input("enter radians: ")) * conversion
    #upper = 2 * math.pi * number_orbits + 0
    thetas = np.arange(0,6 * math.pi + 0.1,0.1).tolist()
    x_values_time = []
    y_values_angle = []
    
    for idx, theta in enumerate(thetas):
        if idx < len(thetas):
            theta = round(theta,3)
            x_values_time.append(time_at_certain_angles((0, theta), h, "1 / (1 - 0.25 * math.cos(x)) ** 2", 'x') * constant_times_integral)
            y_values_angle.append(theta)

    plt.plot(x_values_time,y_values_angle)
    plt.show()
    
    'when the integaral and the constant are multiplied it should give the given answer. the constant is roughly 35/36'


def task6():
    planets: List[Planet] = get_planets()
    planets = [planets[1],planets[2]]
    #planets = [planets[1],planets[3]]
    #planets = [planets[6],planets[7]]

    pygame.init()
    WIN = pygame.display.set_mode((WIDTH,HEIGHT))
    WIN.fill((255,255,255))
    run = True
    clock = pygame.time.Clock()

    frames = 0

    while run and frames < planets[1].ten_rotations_frames_time():
        #print (planets[1].ten_rotations_frames())
        clock.tick(60)
        pygame.display.update()
        frames += 1 #increases by one every frame, counting them

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        togethercoords, locations = planets[0].create_orbit()
        pygame.draw.lines(WIN, planets[0].color, False, togethercoords, 2)
        togethercoords, locations = planets[1].create_orbit()
        pygame.draw.lines(WIN, planets[1].color, False, togethercoords, 2)
        try:
            if frames % round(planets[1].calc_frame_mod()) == 0:
                Planet.match_up_locations(planets[0],planets[1],WIN,frames)
                #print(round(planets[1].calc_frame_mod()))
        except ZeroDivisionError:
            Planet.match_up_locations(planets[0],planets[1],WIN,frames)

        pygame.display.update()

    pygame.quit()


def main():
    task1()
    task2()
    task3()
    task4()
    task5()
    task6()


if __name__ == '__main__':
    main()
    '''
    constant_times_integral = 248.348 * ((1 - 0.0625) ** (3/2)) * (1 / (2*math.pi))
    print (constant_times_integral)
    answer = time_at_certain_angles((0, 6 * math.pi), 0.001, "1 / (1 - 0.25 * math.cos(x)) ** 2", 'x')
    print(answer)
    print(constant_times_integral * answer)
    '''
    #print ((1/1000) / (1 - 0.25 * math.cos(5) ** 2))
    #print (5 / math.pi * 180 / 360 * 248.348)
    #Planet.match_up_locations(planets[0],planets[1])

    