from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np

def plot_results(x_ax, prediction, robot, vicon, smoothed=None, euclidean: bool = False):
    """Plots predictions, robot and vicon X and Y Coordinates and Error over time.

    Args:
        x_ax (np.ndarray): _description_
        prediction (np.ndarray): _description_
        robot (np.ndarray): _description_
        vicon (np.ndarray): _description_
    """

    sns.set(style="whitegrid")
    x_pred = prediction[:,0]
    x_robot = robot[:,0]
    x_vicon = vicon[:,0]

    y_pred = prediction[:,1]
    y_robot = robot[:,1]
    y_vicon = vicon[:,1]

    if smoothed is not None:
        x_pred_smooth = smoothed[:,0]
        y_pred_smooth = smoothed[:,1]

    if euclidean:
        fig, axs = plt.subplots(2,1,sharey='row',figsize=(16,9),layout="constrained")
        # euclidean distance
        dist_pred = np.linalg.norm(prediction,axis=1)
        if smoothed is not None:
            dist_pred_smooth = np.linalg.norm(smoothed,axis=1)
        dist_robot = np.linalg.norm(robot,axis=1)
        dist_vicon = np.linalg.norm(vicon,axis=1)

        axs[0].plot(x_ax,dist_pred , label = "prediction")
        if smoothed is not None:
            axs[0].plot(x_ax,dist_pred_smooth , label = "prediction smooth")
        
        axs[0].plot(x_ax, dist_robot, label="robot")
        axs[0].plot(x_ax, dist_vicon, label="vicon")
        axs[0].set_title("Euclidean Distance", size =16, color='#4f4e4e')
        axs[0].set_ylabel('Position (mm)', size =16, color='#4f4e4e')
        axs[0].legend()
        axs[1].plot(x_ax, dist_vicon-dist_pred, label="prediction")
        
        if smoothed is not None:
            axs[1].plot(x_ax, dist_vicon-dist_pred_smooth, label="prediction smooth")
        axs[1].plot(x_ax, dist_vicon-dist_robot, label = "robot")
        # axs[1,0].set_title("X-Error",  size =16, color='#4f4e4e')
        axs[1].set_ylabel('Error (mm)', size =16, color='#4f4e4e')
        axs[1].axhline(color='#4f4e4e', linestyle = "--")




    else:
        fig, axs = plt.subplots(2,2,sharey='row',figsize=(16,9),layout="constrained")

        axs[0,0].plot(x_ax,x_pred , label = "prediction")
        if smoothed is not None:
            axs[0,0].plot(x_ax,x_pred_smooth , label = "prediction smooth")

        axs[0,0].plot(x_ax, x_robot, label="robot")
        axs[0,0].plot(x_ax, x_vicon, label="vicon")
        axs[0,0].set_title("X-Coordinates", size =16, color='#4f4e4e')
        axs[0,0].set_ylabel('Position (mm)', size =16, color='#4f4e4e')

        axs[0,1].plot(x_ax,y_pred , label = "prediction")
        if smoothed is not None:
            axs[0,1].plot(x_ax,y_pred_smooth , label = "prediction smooth")

        axs[0,1].plot(x_ax, y_robot, label="robot")
        axs[0,1].plot(x_ax, y_vicon, label="vicon")
        axs[0,1].set_title("Y-Coordinates",  size =16, color='#4f4e4e')


        axs[0,1].legend()

        axs[1,0].plot(x_ax, x_vicon-x_pred, label="prediction")
        if smoothed is not None:
            axs[1,0].plot(x_ax, x_vicon-x_pred_smooth, label="prediction smooth")

        axs[1,0].plot(x_ax, x_vicon-x_robot, label = "robot")
        # axs[1,0].set_title("X-Error",  size =16, color='#4f4e4e')
        axs[1,0].set_ylabel('Error (mm)', size =16, color='#4f4e4e')
        axs[1,0].axhline(color='#4f4e4e', linestyle = "--")


        axs[1,1].plot(x_ax, y_vicon-y_pred, label = "prediction")
        if smoothed is not None:
            axs[1,1].plot(x_ax, y_vicon-y_pred_smooth, label = "prediction smooth")

        axs[1,1].plot(x_ax, y_vicon-y_robot, label = "robot")
        # axs[1,1].set_title("Y-Error",  size =16, color='#4f4e4e')
        axs[1,1].axhline(color='#4f4e4e', linestyle = "--")
        plt.legend()

    sns.despine(left=True)


    plt.show()


def plot_results_error(x_ax, prediction, robot, vicon, smoothed=None, euclidean: bool = False):
    """Plots predictions, robot and vicon X and Y Coordinates and Error over time.

    Args:
        x_ax (np.ndarray): _description_
        prediction (np.ndarray): _description_
        robot (np.ndarray): _description_
        vicon (np.ndarray): _description_
    """

    sns.set(style="whitegrid")
    x_pred = prediction[:,0]
    x_robot = robot[:,0]
    x_vicon = vicon[:,0]

    y_pred = prediction[:,1]
    y_robot = robot[:,1]
    y_vicon = vicon[:,1]

    if smoothed is not None:
        x_pred_smooth = smoothed[:,0]
        y_pred_smooth = smoothed[:,1]

    if euclidean:
        fig, axs = plt.subplots(2,1,sharey='row',figsize=(16,9),layout="constrained")
        # euclidean distance
        dist_pred = np.linalg.norm(prediction,axis=1)
        if smoothed is not None:
            dist_pred_smooth = np.linalg.norm(smoothed,axis=1)
        dist_robot = np.linalg.norm(robot,axis=1)
        dist_vicon = np.linalg.norm(vicon,axis=1)

        axs[0].plot(x_ax,dist_pred , label = "prediction")
        if smoothed is not None:
            axs[0].plot(x_ax,dist_pred_smooth , label = "prediction smooth")
        
        axs[0].plot(x_ax, dist_robot, label="robot")
        axs[0].plot(x_ax, dist_vicon, label="vicon")
        axs[0].set_title("Euclidean Distance", size =16, color='#4f4e4e')
        axs[0].set_ylabel('Position (mm)', size =16, color='#4f4e4e')
        axs[0].legend()
        axs[1].plot(x_ax, dist_vicon-dist_pred, label="prediction")
        
        if smoothed is not None:
            axs[1].plot(x_ax, dist_vicon-dist_pred_smooth, label="prediction smooth")
        axs[1].plot(x_ax, dist_vicon-dist_robot, label = "robot")
        # axs[1,0].set_title("X-Error",  size =16, color='#4f4e4e')
        axs[1].set_ylabel('Error (mm)', size =16, color='#4f4e4e')
        axs[1].axhline(color='#4f4e4e', linestyle = "--")




    else:
        fig, axs = plt.subplots(2,2,sharey='row',figsize=(16,9),layout="constrained")

        axs[0,0].plot(x_ax,x_pred + x_robot , label = "prediction")
        if smoothed is not None:
            axs[0,0].plot(x_ax,x_pred_smooth + x_robot , label = "prediction smooth")

        axs[0,0].plot(x_ax, x_robot, label="robot")
        axs[0,0].plot(x_ax, x_vicon, label="vicon")
        axs[0,0].set_title("X-Coordinates", size =16, color='#4f4e4e')
        axs[0,0].set_ylabel('Position (mm)', size =16, color='#4f4e4e')

        axs[0,1].plot(x_ax,y_pred + y_robot , label = "prediction")
        if smoothed is not None:
            axs[0,1].plot(x_ax,y_pred_smooth + y_robot , label = "prediction smooth")

        axs[0,1].plot(x_ax, y_robot, label="robot")
        axs[0,1].plot(x_ax, y_vicon, label="vicon")
        axs[0,1].set_title("Y-Coordinates",  size =16, color='#4f4e4e')


        axs[0,1].legend()

        axs[1,0].plot(x_ax, x_pred, label="prediction")
        if smoothed is not None:
            axs[1,0].plot(x_ax, x_pred_smooth, label="prediction smooth")

        axs[1,0].plot(x_ax, x_vicon - x_robot, label = "robot")
        # axs[1,0].set_title("X-Error",  size =16, color='#4f4e4e')
        axs[1,0].set_ylabel('Error (mm)', size =16, color='#4f4e4e')
        axs[1,0].axhline(color='#4f4e4e', linestyle = "--")


        axs[1,1].plot(x_ax, y_pred, label = "prediction")
        if smoothed is not None:
            axs[1,1].plot(x_ax, y_pred_smooth, label = "prediction smooth")

        axs[1,1].plot(x_ax, y_vicon-y_robot, label = "robot")
        # axs[1,1].set_title("Y-Error",  size =16, color='#4f4e4e')
        axs[1,1].axhline(color='#4f4e4e', linestyle = "--")
        plt.legend()

    sns.despine(left=True)


    plt.show()