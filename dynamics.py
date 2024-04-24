"""
EM 311M DYANMICS WITH DR. CONNOLLY
FINAL VEHICLE CRASH DATA ANALYSIS PROJECT

MADE BY: JIWOONG "ALEX" CHOI
LAST EDITED: SUNDAY APRIL 21, 2024

JESUS LOVES YOU. NO MATTER WHAT.
"""
import matplotlib.pyplot as plt
import numpy as np
import sys
import pylightxl as xl

def open_xl_file(file_name: str = '.xlsx'):
    """ 
    Opens the Excel file and returns the excel file object and returns error if it doesn't
    """
    # import the Excel file 
    try:
        return xl.readxl(file_name)
    # in case the file is not found in the same folder.
    except FileNotFoundError:
        sys.exit("Excel File was not found. Check if it's in the same folder as this Python file.")
    # in case the file is not accessible.
    except PermissionError:
        sys.exit("Excel File couldn't be opened. Make sure the file is allowed to be accessed.")

def read_xl_data(xl_file: xl, worksheet: str, padding:int = 0):
    """
    Reads 2 column data and returns 2 lists

    :param worksheet: worksheet name
    :param padding: number of headers or description cells before actual data cells

    :return: forces array and ADC readings array
    :rtype: np.arrays
    """
    # 1: get time values
    # 1.1: only need numerical values of time, get rid of padding:
    times = xl_file.ws(ws = worksheet).col(1)[padding: ]

    # 2: get acceleration values
    # 2.1: only need numerical values of force, get rid of padding:
    accelerations = xl_file.ws(ws = worksheet).col(2)[padding: ]
    
    # 3: turn them into numpy vectors and return them
    return np.array(times, dtype = float), np.array(accelerations, dtype = float)


# def plot_sensor_data(xl_file: xl, worksheet: str, rows: int = 2, cols: int = 8, linearize: bool = False):
    """
    Scatter plots a figure of all the sensors based on user's desired combination of row and column.
    This also returns values of m(slope) and b(y-intercept)
    """
    # vectors to store slopes and intercepts of best fit lines for each sensor
    slopes = np.zeros(rows * cols)
    intercepts = np.zeros(rows * cols)
    
    # 0: create a desired figure
    fig, axs = plt.subplots(rows, cols, figsize = (16, 6))
    
    # iterate through each subplot:
    for row in range(rows):
        for col in range(cols):
            # set visual-related parameters
            font_size = 9
            font_family = 'Helvetica' 

            # 1: figure out the sensor num
            sensor_num = row * cols + col + 1
            
            # 2: get Force and ADC values for current sensor:
            forces, ADCs = read_sensor_data(xl_file, worksheet, sensor_num, padding)
            # 2.1: if linearization is desired, linearize it.
            if linearize:
                ADCs = linearize_data(ADCs, Resistance, scale_factor = 1000.0)
                # get relevant values
                m, b, R_sq = best_fit_line(forces, ADCs)
                # store slope and y-intercept into corresponding vectors:
                slopes[sensor_num - 1] = m
                intercepts[sensor_num - 1] = b
                # plot the line of best fit:
                axs[row, col].plot(forces, m * forces + b, color = 'k', linestyle = '-')
                # Add legend to the graph
                axs[row, col].legend([f"slope = {m:.2f}\nintercept = {b:.2f}\n$R^2$ = {R_sq:.2f}"], loc = 'upper left', fontsize = font_size - 2)

            
            # 3: plot them
            axs[row, col].scatter(forces, ADCs, s = 7)
            
            # 4: write the apt title
            axs[row, col].set_title(f"Sensor {sensor_num}", fontsize = font_size, fontfamily = font_family)
            
            # 5: write horitzontal and vertical axes names:
            axs[row, col].set_xlabel("Force (Newtons)", fontsize = font_size, fontfamily = font_family)
            axs[row, col].set_ylabel("Cs", fontsize = font_size, fontfamily = font_family)
            
            # 6: Adjust x-axis and y-axis tick labels
            axs[row, col].tick_params(axis = 'x', labelsize = font_size, labelfontfamily = font_family) 
            axs[row, col].tick_params(axis = 'y', labelsize = font_size, labelfontfamily = font_family) 
    
    plt.tight_layout()
    
def plot_data(x1, y1, x2, y2, title: str = 'Title', x_label: str = 'X Label', y_label: str = 'Y Label', legend1: str = 'Case 1', legend2: str = 'Case 2'):
    # pre-set visual related elements:
    font_size = 10
    font_type = 'Arial'
    line_width = 2
    
    # create a new figure
    plt.figure(title)

    # plot both sets of x and y data:
    plt.plot(x1, y1, label = legend1, color = 'lightcoral', linewidth = line_width)
    plt.plot(x2, y2, label = legend2, color = 'cornflowerblue', linewidth = line_width)
    
    # display title, x & y axis labels
    plt.title(title, fontfamily = font_type, fontsize = font_size * 2, fontweight = 'bold') # Title
    plt.xlabel(x_label, fontfamily = font_type, fontsize = font_size, fontweight = 'bold') # X label
    plt.ylabel(y_label, fontfamily = font_type, fontsize = font_size, fontweight = 'bold') # Y label

    # Add gridlines
    plt.grid(True)

    # display graph legend
    plt.legend(prop = {'family': font_type, 'size': font_size, 'weight': 'bold'}, loc = 'lower right')

def numerical_integration(x: np.array, fx: np.array, initial_value: float = 0.0):
    """
    Performs numerical integration using trapzeoidal integration function. 
    Returns newly integrated data points.

    Here is a representation of the calculation of the distance traveled at the end of each time interval, showing the concept of keeping a running total of the are
    𝑑(10) = 𝐴1
    𝑑(20) = 𝐴1 + 𝐴2
    𝑑(30) = 𝐴1 + 𝐴2 + 𝐴3
    .
    .
    .
    𝑑(90) = 𝐴1 + 𝐴2 + 𝐴3 + ⋯ + 𝐴8 + 𝐴9
    𝑑(100) = 𝐴1 + 𝐴2 + 𝐴3 + ⋯ + 𝐴8 + 𝐴9 + 𝐴10
    """
    # error checking:
    if len(x) != len(fx):
        sys.exit("ERROR: x and y vectors are not the same length.")

    # array to keep track of integration value at each intervals:
    areas = np.zeros(len(fx), dtype = float)
    # we already have initial velocity so set that equal to initial area
    areas[0] = initial_value # total_area is used to keep track of total area under the curve
    total_area = initial_value
    
    # we'll interate for each value in x-data while keep the running total.
    for pos in range(1, len(x)):
        # 1: calculate the small (incremental) trapezoid area and add it to the total area
        # formula for trapezoid area is: width / 2 * (height1 + height2)
        total_area += 0.5 * (x[pos] - x[pos - 1]) * (fx[pos] + fx[pos - 1])
        # 2: assign the newly updated integration value to the areas array:
        areas[pos] = total_area
    
    # return the newly integrated data points:
    return areas, total_area


def main():
    ######################## START: EXCEL DATA IMPORT ########################
    # NOTE: Your Excel file must have BOTH case 1 and case 2 data, in two separate sheets. 
    # open the Excel file:
    xl_file = open_xl_file(file_name = 'Dynamics Crash Data.xlsx')

    mass = 0.4 # mass of the vehicle
    v0_1 = 1.8 # initial velocity for Case 1
    v0_2 = 1.6 # initial velocity for Case 2
    
    # collect time and acceleration values for CASE 1:
    times_1, accelerations_1 = read_xl_data(xl_file, worksheet = 'Case 1', padding = 1)
    # collect time and acceleration values for CASE 2:
    times_2, accelerations_2 = read_xl_data(xl_file, worksheet = 'Case 2', padding = 1)

    # use numerical integration to get velocity data:
    velocities_1 = numerical_integration(times_1, accelerations_1, initial_value = v0_1)
    velocities_2 = numerical_integration(times_2, accelerations_2, initial_value = v0_2)

    # and go ahead just calculate the forces as well:
    forces_1 = mass * accelerations_1
    forces_2 = mass * accelerations_2
    ######################## END: EXCEL DATA IMPORT ########################


    ######################## START: KINEMATIC ANALYSIS ########################
    # TODO 1: the acceleration of the vehicle vs. time – plot both cases separately and then on the same set of axes
    # plot_data(times_1, accelerations_1, times_2, accelerations_2, "ACCELERATION of the vehicle VS TIME", 'Time ($s$)', 'Acceleration ($m/s^2$)', 'Case 1', 'Case 2')

    # TODO 2: the force exerted on the vehicle vs. time – plot both cases separately and then on the same set of axes
    # plot_data(times_1, forces_1, times_2, forces_2, "FORCE Exerted on the vehicle VS TIME", 'Time ($s$)', 'Force ($Newtons$)', 'Case 1', 'Case 2')

    # TODO 3: the velocity of the vehicle vs. time for both case
    # plot_data(times_1, velocities_1, times_2, velocities_2, "VELOCITY of the vehicle VS TIME", 'Time ($s$)', 'Velocity ($m/s$)', 'Case 1', 'Case 2')
    ######################## END: KINEMATIC ANALYSIS ########################
    

    ######################## START: IMPULSE AND MOMENTUM ANALYSIS ########################
    # TODO 1: Determine the momentum of the vehicle prior to impact, p1 , for each case
    p0_1 = mass * v0_1
    p0_2 = mass * v0_2
    
    # TODO 2: Determine the momentum of the vehicle after impact, p2 , for each case
    # plot_data(times_1, mass * velocities_1, times_2, mass * velocities_2, "MOMENTUM VS TIME", 'Time ($s$)', 'Momentum ($N-s$)', 'Case 1', 'Case 2')
    pf_1 = mass * velocities_1[-1]
    pf_2 = mass * velocities_2[-1]

    # TODO 3: Determine the total impulse imparted on the vehicle as a result of the collision for both cases 
            # – you should use the numerical integration algorithm discussed in class.
    # total impulse is the area under the curve of Force VS Time
    impulse_1, area1 = numerical_integration(times_1, forces_1, forces_1[0]) # FIXME
    impulse_2, area2 = numerical_integration(times_2, forces_2, forces_2[0]) # FIXME

    impulse_1 = np.trapz(forces_1, times_1)
    impulse_2 = np.trapz(forces_2, times_2)

    print(f"\nTotal Impulse Case 1: {impulse_1}\nTotal Impulse Case 2: {impulse_2}\n")
    print(f"\nDelta P Case 1: {pf_1 - p0_1}\nDelta P Case 2: {pf_2 - p0_2}\n")

    print(area1, area2)

    ######################## END: IMPULSE AND MOMENTUM ANALYSIS ########################


    plt.show()

if __name__ == "__main__":
    main()