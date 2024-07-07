#%reset -f

# <codecell> Module import header

import os
import sys
import cv2
import time
import glob
import pickle
import numpy as np
import matplotlib as mpl
import moviepy.editor as mpy
from collections import deque
from datetime import datetime
from skimage.feature import hog
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import matplotlib.image as mpimg
from sklearn.svm import LinearSVC
import matplotlib.gridspec as gridspec
from scipy.ndimage.measurements import label
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from moviepy.video.io.bindings import mplfig_to_npimage
from sklearn.metrics import confusion_matrix, recall_score
from sklearn.metrics import accuracy_score, precision_score


# <codecell> Helper Functions

# Get sliding window list with scaling
def sliding_windows_list(img, crop_window=((0,400),(1280,660)), overlap=0.5):
    # Define the window size and scales
    window_list = []
    window_size = (64, 64)
    scale_list = [1.0, 1.25, 1.5, 1.75, 2.0]
    #
    X1 = crop_window[0][0] ; X2 = crop_window[1][0]
    Y1 = crop_window[0][1] ; Y2 = crop_window[1][1]
    W = X2 - X1 ; H = Y2 - Y1
    #
    for s in scale_list:
        w = np.int(window_size[0]*s)
        h = np.int(window_size[1]*s)
        sx = np.int(w*(1-overlap)) # x-gap from one window to other
        sy = np.int(h*(1-overlap)) # y-gap from one window to other
        nx = np.int((W-overlap*w)//sx) # number of windows in x
        rx = np.int((W-overlap*w)%sx) # for checking for gap at edges of x-span
        ny = np.int((H-overlap*h)//sy) # number of windows in y
        ry = np.int((H-overlap*h)%sy) # for checking for gap at edges of y-span
        for i in range(nx):
            x1 = i*sx + X1 ; x2 = x1 + w ;  y1 = Y1 ; y2 = y1 + h
            window_list.append(((x1, y1), (x2, y2)))
            # Pprocess for second window in y-direction
            if ny < 2 and ry != 0:
                y2 = Y2 ; y1 = y2 - h
            else:
                y1 = sy + Y1 ; y2 = y1 + h
            window_list.append(((x1, y1), (x2, y2)))
        if rx != 0:
            x2 = X2 ; x1 = x2 - w ; y1 = Y1 ; y2 = y1 + h
            window_list.append(((x1, y1), (x2, y2)))
            # Pprocess for second window in y-direction
            if ny < 2 and ry != 0:
                y2 = Y2 ; y1 = y2 - h
            else:
                y1 = sy + Y1 ; y2 = y1 + h
            window_list.append(((x1, y1), (x2, y2)))
    return window_list

#img = plt.imread('test_images/test6.jpg')
#wlist = sliding_windows_list(img)
#imcopy = np.copy(img)
#for bbox in wlist:
#    cv2.rectangle(imcopy, bbox[0], bbox[1], (0, 0, 255), 6)
#plt.imshow(imcopy)


# <codecell> Search image & classify window

# Define a function you will pass an image 
# and the list of windows to be searched (output of slide_windows())
def find_cars(image, windows):
    
    global nspatial, nhistbin, norients, nhog_ppc, nhog_cpb, fvlength
    global scl, svc, heat_maps # cnt_trace
    on_windows = []
    # Make copy for sliding window and car bounding box visualization
    swbox = np.copy(image) ; cbbox = np.copy(image)
    heat = np.zeros_like(image[:,:,0]).astype(np.float)
    mask = np.ones_like(image[:,:,0]).astype(np.float)
    X = np.empty((0, fvlength))
    for w in windows:
        img = cv2.resize(image[w[0][1]:w[1][1], w[0][0]:w[1][0]], (64, 64))
        img_L = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)[:,:,0]
        spatial_features = cv2.resize(img_L, (nspatial, nspatial)).ravel()
        hist_features = np.histogram(img_L, bins=nhistbin, range=(0, 256))[0]
        hog_features = hog(img_L, orientations=norients,
                           pixels_per_cell=(nhog_ppc,nhog_ppc),
                           cells_per_block=(nhog_cpb, nhog_cpb),
                           transform_sqrt=True, visualise=False,
                           feature_vector=True)
        X = [np.concatenate([spatial_features, hist_features, hog_features])]
        Xscl = scl.transform(np.array(X).reshape(1, -1))
        y = svc.predict(Xscl)
        if y == 1:
            on_windows.append(w)
            cv2.rectangle(swbox, w[0], w[1], (0, 0, 255), 6)
            heat[w[0][1]:w[1][1], w[0][0]:w[1][0]] += 1
    for hm in heat_maps:
        mask = np.logical_and(mask, hm) # only have non-zero values
    mask = np.logical_and(mask, heat)
    heat[mask] = heat[mask] + 5 # add extra heat if present in last three frames
    heat[heat <= 4] = 0 # clean up current false positives
    heat_maps.append(heat) # update heat_map
    labels = label(heat)
    
    # find minimum and maximum of all bounding boxes and plot overall box
    bbox_list = [] ; car_num = 0
    for car in range(1, labels[1]+1):
        nz = (labels[0] == car).nonzero()
        nzy = np.array(nz[0]) ; nzx = np.array(nz[1])
        if (np.max(nzx)-np.min(nzx)) < 64 or (np.max(nzy)-np.min(nzy)) < 64:
            continue # ignore if width or height is less than smallest window
        bbox = ((np.min(nzx), np.min(nzy)),(np.max(nzx), np.max(nzy)))
        bbox_list.append(bbox) ; car_num += 1
        cv2.rectangle(cbbox, bbox[0], bbox[1], (0,0,255), 6)
        cv2.putText(cbbox,'Car {0}'.format(car_num),
                    (bbox[0][0], bbox[1][1]+25),
                    cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,255,255), 2,
                    cv2.LINE_AA, False)
    
    #if bbox_list:
    #    cnt_trace.append(np.average(bbox_list,axis=1))
    #    for clist in cnt_trace:
    #        for c in clist:
    #            cv2.circle(cbbox, (int(c[0]), int(c[1])), 10, (0,255,0), -1)
    
    return bbox_list, swbox, cbbox

#img = plt.imread('test_images/test6.jpg')
#wlist = sliding_windows_list(img)
#bbox_list, swbox_img, cbbox_img = find_cars(img, wlist)
#plt.imshow(swbox_img)
#plt.imshow(heat_maps[-1], cmap='hot')
#plt.imshow(cbbox_img)


# <codecell> Helper function for making MoviePy frame

def make_frame(t):
    
    global nspatial, nhistbin, norients, nhog_ppc, nhog_cpb, fvlength
    global scl, svc, heat_maps # cnt_trace
    # Load image for testing
    #img = cv2.imread('./test_images/straight_lines1.jpg')
    
    # Open a file for logging debug output
    if debug_log:
        with open("log.txt", "a") as myfile:
            myfile.write('\n ====== {:.2f} ======'.format(t))
    
    # Load the frame from video clip for processing
    img = src_clip.get_frame(t)
    
    wlist = sliding_windows_list(img)
    bbox_list, swbox_img, cbbox_img = find_cars(img, wlist)
    
    if bbox_list:
        w = bbox_list[0]
        plot_img = cv2.cvtColor(cv2.resize(
            img[bbox_list[0][0][1]:w[1][1], bbox_list[0][0][0]:w[1][0]], (64, 64)),
            cv2.COLOR_RGB2LAB)[:,:,0]
        hog_features, hog_img = hog(plot_img, orientations=norients,
                           pixels_per_cell=(nhog_ppc,nhog_ppc),
                           cells_per_block=(nhog_cpb, nhog_cpb),
                           transform_sqrt=True, visualise=True,
                           feature_vector=True)
    else:
        plot_img = Image.new("RGBA",(64,64),"gray")
        draw = ImageDraw.Draw(plot_img)
        w, h = draw.textsize("NO CAR")
        draw.text(((64-w)/2,(64-h-10)/2), "NO CAR", fill="black")
        w, h = draw.textsize("FOUND")
        draw.text(((64-w)/2,(64-h+10)/2), "FOUND", fill="black")
        hog_img = np.copy(plot_img)
    
    # 5. Assemble the sub-plot style figure for project output submission
    fig = plt.figure(figsize=(18, 12))
    gs = gridspec.GridSpec(3, 3)
    ax1 = fig.add_subplot(gs[0:2, 0:2])
    ax2 = fig.add_subplot(gs[0,2])
    ax3 = fig.add_subplot(gs[1,2])
    ax4 = fig.add_subplot(gs[2,2])
    ax5 = fig.add_subplot(gs[2,1])
    ax6 = fig.add_subplot(gs[2,0])
    
    # Axes 1: Bounding box and trailing dot trace in time
    ax1.imshow(cbbox_img, cmap='gray')
    ax1.set_title('Bounding Box and Trace', fontsize=16)
    
    # Axes 2: Original Image
    ax2.imshow(img, cmap='gray')
    ax2.set_title('Original Image', fontsize=16)
    
    # Axes 3: All detected sliding windows
    ax3.imshow(swbox_img, cmap='gray')
    ax3.set_title('Detected Sliding Windows', fontsize=16)
    
    # Axes 4: Heat map
    ax4.imshow(heat_maps[-1], cmap='hot')
    ax4.set_title('Heat Map', fontsize=16)
    
    # Axes 5: Example HOG Image
    ax5.imshow(hog_img, cmap='gray')
    ax5.set_title('HOG Image', fontsize=16)
    
    # Axes 6: Example plot of identified car
    ax6.imshow(plot_img, cmap='gray')
    ax6.set_title('Plot Image', fontsize=16)
    
    fig.tight_layout()
    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
    
    #cv2.imwrite('lane_detection.jpg', mplfig_to_npimage(fig))
    #plt.imsave('lane_detection.jpg', mplfig_to_npimage(fig))
    #cv2.imshow('img',mplfig_to_npimage(fig))
    
    # Save the figure to output directory for backup or GIF creation & return
    fig.savefig('output_images/vehicle_detection{:.2f}.jpg'.format(t),
                bbox_inches='tight')
    output = mplfig_to_npimage(fig)
    # Following line prevents the figure echo in the IPython console
    plt.close(fig)
    
    return output


# <codecell> Load training and test data

# Read in cars and notcars
cars = glob.glob('vehicles/*/*.jp*')
notcars = glob.glob('non_vehicles/*/*.jp*')

# Parameter set for tuning
nspatial = 16 ; nhistbin = 16 ; norients = 9 ; nhog_ppc = 8 ; nhog_cpb = 2
# Calculate the feature vector length per image
fvlength = nspatial**2 + nhistbin + (nhog_ppc-1)**2 * nhog_cpb**2 * norients

#1) Define an empty list to receive features
#2) Apply color conversion if other than 'RGB'
#3) Compute spatial features if flag is set and append to image features
#5) Compute histogram features if flag is set and append to image features
#7) Compute HOG features if flag is set and append to image features
#8) Append features to list
#9) Return concatenated array of features
    
if os.path.exists('./train_data.p'):
    train_data = pickle.load(open('./train_data.p', 'rb'))
    Xscl = train_data['x_data']
    y = train_data['y_data']
    scl = train_data['scaler']
else:
    X = np.empty((0, fvlength))
    for file in cars+notcars:
        img = mpimg.imread(file)
        img_L = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)[:,:,0]
        spatial_features = cv2.resize(img_L, (nspatial, nspatial)).ravel()
        hist_features = np.histogram(img_L, bins=nhistbin, range=(0, 256))[0]
        hog_features = hog(img_L, orientations=norients,
                           pixels_per_cell=(nhog_ppc,nhog_ppc),
                           cells_per_block=(nhog_cpb, nhog_cpb),
                           transform_sqrt=True, visualise=False,
                           feature_vector=True)
        X = np.append(X, [np.concatenate([spatial_features,
                                          hist_features,
                                          hog_features])], axis=0)
    # Fit a per-column scaler
    scl = StandardScaler().fit(X)
    # Apply the scaler to X
    Xscl = scl.transform(X)
    # Define the labels vector
    y = np.hstack((np.ones(len(cars)), np.zeros(len(notcars))))
    # Dump data to the file
    pfile = open('./train_data.p','wb')
    pickle.dump({'x_data':Xscl, 'y_data':y, 'scaler':scl}, pfile)


# <codecell> Train and test SVM classifier

# Split up data into randomized training and test sets
rand_state = np.random.randint(0, 100)
X_train, X_test, y_train, y_test = train_test_split(Xscl, y,
                                                    test_size=0.2,
                                                    random_state=rand_state)

svc = LinearSVC()
t=time.time()
svc.fit(X_train, y_train)
t2 = time.time()
print(round(t2-t, 2), 'Seconds to train SVC...')
print('Test Accuracy of SVC = {0:4f}'.format(svc.score(X_test, y_test)))
y_predict = svc.predict(X_test)
print('SCV Accuracy = {0:4f}'.format(accuracy_score(y_test, y_predict)))
print('SCV Precision = {0:4f}'.format(precision_score(y_test, y_predict)))
print('SCV Recall = {0:4f}'.format(recall_score(y_test, y_predict)))
print('Confusion Matrix:')
print(confusion_matrix(y_test, y_predict))


# <codecell> Script main code

# Prevent plot figure pop-up and print to IPython console
plt.ioff()
#mpl.use('Agg')

debug_log = True
if debug_log:
    with open('log.txt', 'w') as myfile:
        myfile.write('\n\n ##### Log @ {} ##### \n\n'.format(datetime.now()))

src_vid = mpy.VideoFileClip('project_video.mp4', audio=False)
start_time = 0.0 ; end_time = None
src_clip = src_vid.subclip(t_start=start_time, t_end=end_time)

heat_maps = deque(maxlen=3)
heat_maps.append(np.ones_like(src_vid.get_frame(0)[:,:,0]))
#cnt_trace = deque(maxlen=10)

dst_clip = mpy.VideoClip(make_frame, duration=src_clip.duration)
dst_clip.write_videofile('project_output.mp4', fps=src_vid.fps)

# Reset IPython console settings to original
plt.ion()
