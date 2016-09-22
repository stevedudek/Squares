/*
  Square Simulator and Lighter
  
  1. Simulator: draws squares on the monitor
  2. Lighter: sends data to the lights
  
  Includes Tiling of
  Multiple Big Square Grids
  
  9/22/16
  
  Main parameter is square PIXEL_WIDTH, or number of squares on the base
  PIXEL_WIDTH is fixed at 12 for 144 total squares.
  
  x,y coordinates are weird for each square, but selected to make
  both neighbors and linear movement easier. Turn on the coordinates
  to see the system.
  
  Number of Big Squares set by numBigSquare. Each Big Squares needs
  an (x,y) coordinate and a (Corner, L/R) connector designation. 
  
  Function included to translate x,y coordinates into which number light on which strand.
*/

int numBigSquare = 4;  // Number of Big Squares

// Relative coordinates for the Big Squares
int[][] BigSquareCoord = {
  {0,0},  // Square 1
  {1,0},  // Square 2
  {0,1},  // Square 3
  {1,1}  // Square 4
};

// Matrix listing where the connector attaches physically to each Big Square.
// First value is Corner (Pixel 0) of connector attachment:
// 'Z' = Bottom-Left, 'A' = Top-Left, 'X' = Bottom-Right, 'S' = Top-Right
// Second value is Direction of lights (0->1) from connector as viewed from corner:
// 'L' = Left, 'R' = Right
char[][] connectors = {
  {'Z','R'},  // Square 1
  {'A','R'},  // Square 2
  {'A','L'},  // Square 3
  {'Z','L'}   // Square 4
};

// Wiring diagram - needs to be the same for all fabricated Squares
int[][] LED_LOOKUP = {
  {144, 141, 140, 137, 136, 133, 132, 129, 128, 125, 124, 122},  // 12
  {143, 142, 139, 138, 135, 134, 131, 130, 127, 126, 123, 121},  // 11
  {98, 100, 101, 104, 105, 108, 109, 112, 113, 116, 117, 120},  // 10
  {97, 99, 102, 103, 106, 107, 110, 111, 114, 115, 118, 119},  //  9
  {96, 93, 92, 89, 88, 85, 84, 81, 80, 77, 76, 74},  //  8
  {95, 94, 91, 90, 87, 86, 83, 82, 79, 78, 75, 73},  //  7
  {50, 52, 53, 56, 57, 60, 61, 64, 65, 68, 69, 72},  //  6
  {49, 51, 54, 55, 58, 59, 62, 63, 66, 67, 70, 71},  //  5
  {48, 46, 43, 42, 39, 38, 35, 34, 31, 30, 27, 26},  //  4
  {47, 45, 44, 41, 40, 37, 36, 33, 32, 29, 28, 25},  //  3
  {2, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24},  //  2
  {1, 3, 6, 7, 10, 11, 14, 15, 18, 19, 22, 23}   //  1
};

import com.heroicrobot.dropbit.registry.*;
import com.heroicrobot.dropbit.devices.pixelpusher.Pixel;
import com.heroicrobot.dropbit.devices.pixelpusher.Strip;
import com.heroicrobot.dropbit.devices.pixelpusher.PixelPusher;
import com.heroicrobot.dropbit.devices.pixelpusher.PusherCommand;

import processing.net.*;
import java.util.*;
import java.util.regex.*;
import processing.video.*;  // For video

// network vars
int port = 4444;
Server _server; 
StringBuffer _buf = new StringBuffer();

class TestObserver implements Observer {
  public boolean hasStrips = false;
  public void update(Observable registry, Object updatedDevice) {
    println("Registry changed!");
    if (updatedDevice != null) {
      println("Device change: " + updatedDevice);
    }
    this.hasStrips = true;
  }
}

TestObserver testObserver;

// Physical strip registry
DeviceRegistry registry;

//
// Controller on the bottom of the screen
//
// Draw labels has 3 states:
// 0:LED number, 1:(x,y) coordinate, and 2:none
int DRAW_LABELS = 2;

// Tiling! true means draw all the Big Squares. false means all Big Squares overlap
boolean TILING = true;

int BRIGHTNESS = 100;  // A percentage

int COLOR_STATE = 0;  // no enum types in processing. Messy

// How many little squares on the base of each big square
int PIXEL_WIDTH = 12;  // Height & width in pixels (LEDs) of each square
int NUM_PIXELS = PIXEL_WIDTH * PIXEL_WIDTH;

// Color buffers: [x][y][r,g,b]
// Two buffers permits updating only the lights that change color
// May improve performance and reduce flickering
int pix_width = (int)(grid_width() * PIXEL_WIDTH);  // x-axis for buffer
int pix_height = (int)(grid_height() * PIXEL_WIDTH);  // y-axis for buffer

char[][][] curr_buffer = new char[pix_width][pix_height][3];
char[][][] next_buffer = new char[pix_width][pix_height][3];
char[][][] morph_buffer = new char[pix_width][pix_height][3];

// Calculated pixel constants for simulator display
int SCREEN_SIZE = 600;  // square screen
float SMALL_SIZE = (SCREEN_SIZE - 20) / (PIXEL_WIDTH * grid_width());  // Size of a small square
int BIG_SIZE = (int)(PIXEL_WIDTH * SMALL_SIZE);  // Width of one big square
int SCREEN_WIDTH = (int)(BIG_SIZE * grid_width()) + 20;  // Width + a little
int SCREEN_HEIGHT = (BIG_SIZE * grid_height()) + 20; // Height + a little
int CORNER_X = 10; // bottom left corner position on the screen
int CORNER_Y = SCREEN_HEIGHT - 10; // bottom left corner position on the screen

SquareForm squareGrid;  // Grid model of Big Squares

int delay_time = 10000;  // delay time length in milliseconds (dummy initial value)
int start_time = millis();  // start time point (in absolute time)
int last_time = start_time;

//
// Video variables
//
PImage movieFrame;            // The current movie frame
//PImage displayFrame;          // What is displayed on the Squares
boolean VIDEO_STATE = false;  // Whether video is playing
Movie myMovie;                // The current animated gif
int movie_number;             // current movie number
//int MOVIE_SIZE = 500;   // Maximum 500 x 500 pixel gif animations
int PIX_DENSITY = 10;  // How many screen-pixels wide is each little square
int FRAME_WIDTH = pix_width * PIX_DENSITY;
int FRAME_HEIGHT = pix_height * PIX_DENSITY;
float[] movie_speeds = { 0.0, 0.2, 0.4, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0 };
String[] movie_titles = { "penguin", "Earth", "banana", "bluedot", "nyancat" };

//
// Pixel Array routines
//
class Coord {
  public int x, y;
  
  Coord(int x, int y) {
    this.x = x;
    this.y = y;
  }
}

class RGBColor {
  public float r, g, b;
  
  RGBColor(float r, float g, float b) {
    this.r = r;
    this.g = g;
    this.b = b;
  }
}

class Pixel {
  public int numitems;
  public RGBColor pixcolor;
  
  Pixel() {
    this.numitems = 0;
    pixcolor = new RGBColor(0,0,0);
  }
  
  void Empty() {
    this.numitems = 0;
    pixcolor = new RGBColor(0,0,0);
  }
}

class PixelArray {
  public int width;
  public int height;
  public Pixel[][] Pixels;
  
  PixelArray(int array_width, int array_height) {  // x,y
    this.width = array_width;
    this.height = array_height;
    this.Pixels = new Pixel[array_width][array_height];
    
    for (int y = 0; y < array_height; y++) {
      for (int x = 0; x < array_width; x++) {
        Pixels[x][y] = new Pixel();
      }
    }
    //BlackAllPixels();
  }
  
  boolean IsValidCoord(int x, int y) {
    if (x < 0 || x >= this.width || y < 0 || y >= this.height) {
      return false;  // Out of range
    } else {
      return true;
    }
  }
  
  void EmptyAllPixels() {
    for (int y = 0; y < this.height; y++) {
      for (int x = 0; x < this.width; x++) {
        Pixels[x][y].Empty();
      }
    }
  }
  
  RGBColor GetPixelColor(int x, int y) {
    if (IsValidCoord(x,y)) {
      return Pixels[x][y].pixcolor;
    } else {
      RGBColor black = new RGBColor(0,0,0);
      return black;
    }
  }
     
  void StuffPixelWithColor(int x, int y, RGBColor rgb) {
    if (!IsValidCoord(x,y)) return;  // Out of range
    
    int numdata = Pixels[x][y].numitems;
    if (numdata == 0) {  // First value in pixel. Stuff all of it.
      this.Pixels[x][y].pixcolor = new RGBColor(rgb.r, rgb.g, rgb.b);
    } else {  // Already values in pixel. Do a weighted average with the new value.
      this.Pixels[x][y].pixcolor = new RGBColor(
        (rgb.r + (this.Pixels[x][y].pixcolor.r*numdata))/(numdata+1),
        (rgb.g + (this.Pixels[x][y].pixcolor.g*numdata))/(numdata+1),
        (rgb.b + (this.Pixels[x][y].pixcolor.b*numdata))/(numdata+1));
    }
    this.Pixels[x][y].numitems++;
  }
}

// Buffer that holds [x][y] rectangular pixels
PixelArray pixelarray;

void setup() {
  size(SCREEN_WIDTH, SCREEN_HEIGHT + 50); // 50 for controls
  colorMode(RGB, 255);
  stroke(0);
  fill(255,255,0);
  background(200);  // gray
  frameRate(20); // default 60 seems excessive
  
  squareGrid = makeSquareGrid();  // Set up the Big Squares and stuff in the little squares
  
  registry = new DeviceRegistry();
  testObserver = new TestObserver();
  registry.addObserver(testObserver);
  prepareExitHandler();
  
  initializeColorBuffers();  // Stuff with zeros (all black)
  
  // Image handling
  pixelarray = new PixelArray(pix_width, pix_height);
  
  movieFrame = createImage(FRAME_WIDTH, FRAME_HEIGHT, RGB);
  //movieFrame = createImage(MOVIE_SIZE, MOVIE_SIZE, RGB);
  movie_number = int(random(movie_titles.length));  // Initial movie
  
  _server = new Server(this, port);
  println("server listening:" + _server);
}

void draw() {
  if (VIDEO_STATE) {
    DumpMovieIntoPixels();
    movePixelsToBuffer();
    pixelarray.EmptyAllPixels();
  }
  pollServer();
  update_morph();
    
  drawBigFrames();
  drawBottomControls();
}

void DumpMovieIntoPixels() {
  movieFrame.loadPixels();
  //image(movieFrame, 0, 0);
  // Iterate over background/main image pixel-by-pixel
  // For each pixel, determine the triangular coordinate
  // Width/height ratio is already properly scaled
  for (int j = 0; j < movieFrame.height; j++) {
    for (int i = 0; i < movieFrame.width; i++) {
      Coord coord = GetPixelCoord(i, j, movieFrame.height, movieFrame.width);
      if (!pixelarray.IsValidCoord(coord.x,coord.y)) continue;
      
      // Pull pixel location and color from picture
      int imageloc = i + j*movieFrame.width;
      RGBColor rgb = new RGBColor(red(movieFrame.pixels[imageloc]),
                                 green(movieFrame.pixels[imageloc]),
                                blue(movieFrame.pixels[imageloc]));
                                
      pixelarray.StuffPixelWithColor(coord.x, coord.y, rgb);
    }
  }
}

void movieEvent(Movie m) {
  boolean width_dominate = true;
  
  m.read();        // Get the next movie frame
  m.loadPixels();  // Load frame into memory
  
  // Black out movieFrame - May need to restore this
  /*
  for (int i=0; i < movieFrame.pixels.length; i++) {
    movieFrame.pixels[i] = color(0,0,0);
  }
  */
  
  // Is the "m" movie too wide?
  if ( (m.width/m.height) > (FRAME_WIDTH / FRAME_HEIGHT) ) {
    int new_height = int(movieFrame.width * m.height / m.width);
    
    movieFrame.copy(m,0,0,m.width,m.height, // (src,sx,sy,sw,sh
      0, (movieFrame.height-new_height)/2,  // dx,dy
      movieFrame.width,new_height);         // dw,dh) 

  } else {  // No - make height the dominate value
    int new_width = int(movieFrame.height * m.width / m.height);
    
    movieFrame.copy(m,0,0,m.width,m.height, // (src,sx,sy,sw,sh
      (movieFrame.width-new_width)/2, 0,    // dx,dy 
      new_width,movieFrame.height);         // dw,dh)
  }
}

void turnOnMovie() {
  String movieName = movie_titles[movie_number] + ".mov";
  println("Starting " + movieName);
  myMovie = new Movie(this, movieName);
  myMovie.loop();
}

void nextMovie() {
  myMovie.stop();
  movie_number = (movie_number + 1) % movie_titles.length;
  turnOnMovie();
}

Strip[] set_up_strips(List<Strip> strip_list) {
  // Messy conversion of a strip list to a strip array
  byte counter = 0;
  Strip[] strip_array = new Strip[numBigSquare];
  for (Strip strip : strip_list) {
    if (counter < numBigSquare) {
      strip_array[counter] = strip;
      counter++;
    }
  }
  return strip_array;
}

void drawCheckbox(int x, int y, int size, color fill, boolean checked) {
  stroke(0);
  fill(fill);  
  rect(x,y,size,size);
  if (checked) {    
    line(x,y,x+size,y+size);
    line(x+size,y,x,y+size);
  }  
}

void drawBottomControls() {
  // draw a bottom white region
  fill(255,255,255);
  rect(0,SCREEN_HEIGHT,SCREEN_WIDTH,40);
  
  // draw divider lines
  stroke(0);
  line(140,SCREEN_HEIGHT,140,SCREEN_HEIGHT+40);
  line(290,SCREEN_HEIGHT,290,SCREEN_HEIGHT+40);
  line(470,SCREEN_HEIGHT,470,SCREEN_HEIGHT+40);
  line(630,SCREEN_HEIGHT,630,SCREEN_HEIGHT+40);
  
  // draw checkboxes
  stroke(0);
  fill(255);
  
  // Checkbox is always unchecked; it is 3-state
  rect(20,SCREEN_HEIGHT+10,20,20);  // label checkbox
  
  rect(200,SCREEN_HEIGHT+4,15,15);  // minus brightness
  rect(200,SCREEN_HEIGHT+22,15,15);  // plus brightness
  
  drawCheckbox(340,SCREEN_HEIGHT+4,15, color(255,0,0), COLOR_STATE == 1);
  drawCheckbox(340,SCREEN_HEIGHT+22,15, color(255,0,0), COLOR_STATE == 4);
  drawCheckbox(360,SCREEN_HEIGHT+4,15, color(0,255,0), COLOR_STATE == 2);
  drawCheckbox(360,SCREEN_HEIGHT+22,15, color(0,255,0), COLOR_STATE == 5);
  drawCheckbox(380,SCREEN_HEIGHT+4,15, color(0,0,255), COLOR_STATE == 3);
  drawCheckbox(380,SCREEN_HEIGHT+22,15, color(0,0,255), COLOR_STATE == 6);
  
  drawCheckbox(400,SCREEN_HEIGHT+10,20, color(255,255,255), COLOR_STATE == 0);
  
  drawCheckbox(480,SCREEN_HEIGHT+10,20, color(255,255,255), VIDEO_STATE); // Video
  rect(540,SCREEN_HEIGHT+10,20,20);  // next gif box
  
  
  // draw text labels in 12-point Helvetica
  fill(0);
  textAlign(LEFT);
  PFont f = createFont("Helvetica", 12, true);
  textFont(f, 12);  
  text("Toggle Labels", 50, SCREEN_HEIGHT+25);
  
  text("+", 190, SCREEN_HEIGHT+16);
  text("-", 190, SCREEN_HEIGHT+34);
  text("Brightness", 225, SCREEN_HEIGHT+25);
  textFont(f, 20);
  text(BRIGHTNESS, 150, SCREEN_HEIGHT+28);
  
  textFont(f, 12);
  text("None", 305, SCREEN_HEIGHT+16);
  text("All", 318, SCREEN_HEIGHT+34);
  text("Color", 430, SCREEN_HEIGHT+25);
  text("Video", 505, SCREEN_HEIGHT+25);
  text("Next", 565, SCREEN_HEIGHT+16);
  text("gif", 570, SCREEN_HEIGHT+32);
  
  // scale font to size of squares
  int font_size = 8;  // default size
  f = createFont("Helvetica", font_size, true);
  textFont(f, font_size);
  
}

void mouseClicked() {  
  //println("click! x:" + mouseX + " y:" + mouseY);
  if (mouseX > 20 && mouseX < 40 && mouseY > SCREEN_HEIGHT+10 && mouseY < SCREEN_HEIGHT+30) {
    // clicked draw labels button
    DRAW_LABELS = (DRAW_LABELS + 1) % 3;
   
  }  else if (mouseX > 200 && mouseX < 215 && mouseY > SCREEN_HEIGHT+22 && mouseY < SCREEN_HEIGHT+37) {
    // Bright down checkbox
    BRIGHTNESS -= 5;  
    if (BRIGHTNESS < 1) BRIGHTNESS = 1;
   
  } else if (mouseX > 200 && mouseX < 215 && mouseY > SCREEN_HEIGHT+4 && mouseY < SCREEN_HEIGHT+19) {
    // Bright up checkbox
    if (BRIGHTNESS <= 95) BRIGHTNESS += 5;
  
  }  else if (mouseX > 400 && mouseX < 420 && mouseY > SCREEN_HEIGHT+10 && mouseY < SCREEN_HEIGHT+30) {
    // No color correction  
    COLOR_STATE = 0;
   
  }  else if (mouseX > 340 && mouseX < 355 && mouseY > SCREEN_HEIGHT+4 && mouseY < SCREEN_HEIGHT+19) {
    // None red  
    COLOR_STATE = 1;
   
  }  else if (mouseX > 340 && mouseX < 355 && mouseY > SCREEN_HEIGHT+22 && mouseY < SCREEN_HEIGHT+37) {
    // All red  
    COLOR_STATE = 4;
   
  }  else if (mouseX > 360 && mouseX < 375 && mouseY > SCREEN_HEIGHT+4 && mouseY < SCREEN_HEIGHT+19) {
    // None blue  
    COLOR_STATE = 2;
   
  }  else if (mouseX > 360 && mouseX < 375 && mouseY > SCREEN_HEIGHT+22 && mouseY < SCREEN_HEIGHT+37) {
    // All blue  
    COLOR_STATE = 5;
   
  }  else if (mouseX > 380 && mouseX < 395 && mouseY > SCREEN_HEIGHT+4 && mouseY < SCREEN_HEIGHT+19) {
    // None green  
    COLOR_STATE = 3;
   
  }  else if (mouseX > 380 && mouseX < 395 && mouseY > SCREEN_HEIGHT+22 && mouseY < SCREEN_HEIGHT+37) {
    // All green  
    COLOR_STATE = 6;
    
  }  else if (mouseX > 480 && mouseX < 500 && mouseY > SCREEN_HEIGHT+10 && mouseY < SCREEN_HEIGHT+30) {
    // clicked video button
    VIDEO_STATE = !VIDEO_STATE;
    if (VIDEO_STATE) {
      turnOnMovie();
    } else {
      myMovie.stop();
    }
   
  } else if (mouseX > 540 && mouseX < 560 && mouseY > SCREEN_HEIGHT+10 && mouseY < SCREEN_HEIGHT+30) {
    // clicked next gif button
    if (VIDEO_STATE) nextMovie();
   
  }
}

// Find the square coordinate of an x,y point

Coord GetPixelCoord(int x, int y, int imageHeight, int imageWidth) {
  // Calculate the size of each little square bin
  float sq_height = imageHeight / pix_height;
  float sq_width = imageWidth / pix_width;
  
  // Need to flip y coordinate
  return (new Coord((int)(x / sq_width), pix_width - (int)(y / sq_height) - 1));
}

// Get helper functions
//
// Makes code more readable
// No out-of-bounds error handling. Make sure grid# is valid!
int getBigX(int grid) { return (BigSquareCoord[grid][0]); }
int getBigY(int grid) { return (BigSquareCoord[grid][1]); }
char getConnector(int grid) { return (connectors[grid][0]); }
char getLightDir(int grid) { return (connectors[grid][1]); }

//
// minBigX
//
// Smallest BigX value
int minBigX() {
  int min_x = getBigX(0);
  for (int i=1; i<numBigSquare; i++) {
    if (getBigX(i) < min_x) min_x = getBigX(i);
  }
  return min_x;
}

//
// minBigY
//
// Smallest BigY value
int minBigY() {
  int min_y = getBigY(0);
  for (int i=1; i<numBigSquare; i++) {
    if (getBigY(i) < min_y) min_y = getBigY(i);
  }
  return min_y;
}

//
// grid_width
//
// How many squares across is the big grid?
float grid_width() {
  
  if (TILING == false) return 1;  // Want just one grid
  
  int min_x = getBigX(0);
  int max_x = min_x;
  int new_x;
  
  for (int i=1; i<numBigSquare; i++) {
    new_x = getBigX(i);
    if (new_x < min_x) min_x = new_x;
    if (new_x > max_x) max_x = new_x;
  }
  return (max_x - min_x + 1);
}

//
// grid_height
//
// How many squares high is the big grid?
int grid_height() {
  
  if (TILING == false) return 1;
  
  int min_y = getBigY(0);
  int max_y = min_y;
  int new_y;
  
  for (int i=1; i<numBigSquare; i++) {
    new_y = getBigY(i);
    if (new_y < min_y) min_y = new_y;
    if (new_y > max_y) max_y = new_y;
  }
  return (max_y - min_y + 1);
}

//
// Converts an x,y square coordinate into a (strip, LED) light coordinate
//
int GetLightFromCoord(int x, int y, int grid) {
  // Remove big-grid offsets
  x -= getBigX(grid) * PIXEL_WIDTH;
  y -= getBigY(grid) * PIXEL_WIDTH;
  
  if (x < 0 || x >= PIXEL_WIDTH || y < 0 || y >= PIXEL_WIDTH) {
    return 0;
  }
  
  int new_x, new_y, temp;
  
  if (getLightDir(grid) == 'R') {
    temp = x;
    x = y;
    y = temp;
  }
  
  if (getConnector(grid) == 'A') {
    new_x = PIXEL_WIDTH - x - 1;
    new_y = PIXEL_WIDTH - y - 1; 
  } else if (getConnector(grid) == 'S') {
    new_x = x;
    new_y = PIXEL_WIDTH - y - 1;  
  } else if (getConnector(grid) == 'X') {
    new_x = x;
    new_y = y;
  } else {
    new_x = PIXEL_WIDTH - x - 1;
    new_y = y;
  }
  
  if (getLightDir(grid) == 'R' && (getConnector(grid) == 'A' || getConnector(grid) == 'X')) {
    temp = new_x;
    new_x = new_y;
    new_y = temp;
  }
  
  return LED_LOOKUP[new_x][new_y] - 1;
}

//
// SquareForm class holds an 2D-array of Squares (another class) 
//
SquareForm makeSquareGrid() {
  float pix_x, pix_y;
  
  SquareForm form = new SquareForm(pix_width, pix_height);
  
  for (int i = 0; i < numBigSquare; i++) {
    // Coordinates of a big square
    int big_x = getBigX(i);
    int big_y = getBigY(i);
  
    // small square coordinate offsets 
    int x_offset = big_x * PIXEL_WIDTH;
    int y_offset = big_y * PIXEL_WIDTH;
    
    // screen pixel offsets for the lower-left corner of the big square
    int pix_x_offset = CORNER_X + ((big_x - minBigX()) * BIG_SIZE);  
    int pix_y_offset = CORNER_Y - ((big_y - minBigY()) * BIG_SIZE);
    
    for (int y = 0; y < PIXEL_WIDTH; y++) {  // columns
      for (int x = 0; x < PIXEL_WIDTH; x++) {  // rows
        // Calculate where to draw the pixel square on the screen
        pix_x = pix_x_offset + (x * SMALL_SIZE);
        pix_y = pix_y_offset - ((y+1) * SMALL_SIZE);
        form.add(new Square(pix_x, pix_y, x + x_offset, y + y_offset, i), x + x_offset, y + y_offset);
      }
    }
  }
  return form;  
}


class SquareForm {
  Square[][] squares;
  int x_width;
  int y_height;
  
  SquareForm(int x, int y) {
    this.squares = new Square[x][y];
    this.x_width = x;
    this.y_height = y;
  }
  
  boolean InBounds(int x, int y) {
    return (x >= 0 && x < this.x_width && y >= 0 && y < this.y_height);
  }
  
  void add(Square s, int x, int y) {
    if (InBounds(x, y)) {
      this.squares[x][y] = s;
    }
  }
  
  int getStrip(byte x, byte y) {
    return this.squares[x][y].strip;
  }
  
  int getLED(byte x, byte y) {
    return this.squares[x][y].LED;
  }
  
  void draw() {
    for (byte x = 0; x < this.x_width; x++) {
      for (byte y = 0; y < this.y_height; y++) {
        if (squareExists(x,y)) {
          this.squares[x][y].draw();
        }
      }
    }
  }
  
  void setCellColor(color c, byte x, byte y) {
    if (InBounds(x, y)) { 
      this.squares[x][y].setColor(c);
    }
  }
  
  boolean squareExists(byte x, byte y) {
    return (InBounds(x, y) && this.squares[x][y] != null);
  }
}

/*
 *  Square shape primitives
 */
class Square {
  String id = null; // "xcoord, ycoord"
  int x;  // x in the square array
  int y;  // y in the square array
  float pix_x;  // x-coordinate in pixels on the screen
  float pix_y;  // y-coordinate in pixels on the screen
  int strip; // strip number
  int LED;     // LED number on the strand
  color c;  // color
  
  Square(float pix_x, float pix_y, int x, int y, int strip) {
    this.x = x;
    this.y = y;
    this.pix_x = pix_x;
    this.pix_y = pix_y;
    this.strip = strip;
    this.LED = GetLightFromCoord(x, y, strip);
    this.c = color(255,255,255);
    
    int[] coords = new int[2];
    coords[0] = x;
    coords[1] = y;
    this.id = join(nf(coords, 0), ",");
  }
  
  void setColor(color c) {
    this.c = c;
  }
   
  void draw() {
    fill(c);
    stroke(0);
    rect(this.pix_x, this.pix_y, SMALL_SIZE, SMALL_SIZE);
    
    // toggle text label between light number and x,y coordinate
    String text = "";
    switch (DRAW_LABELS) {
      case 0:
        int[] coords = new int[2];
        coords[0] = this.strip;
        coords[1] = this.LED;
        text = join(nf(coords, 0), ",");
        break;
      case 1:
        text = this.id;  // (x,y) coordinate
        break;
      case 2:
        break;  // no label
    }
    
    if (this.id != null) {
      fill(0);
      textAlign(CENTER);
      text(text, this.pix_x + SMALL_SIZE/2, this.pix_y + SMALL_SIZE/2);
    }
    noFill();
  }
}

//
// drawBigFrames
//
// Draws a big bold square around each grid

void drawBigFrames() {
  noFill();
  strokeWeight(5);
  int x_coord, y_coord;
  
  for (byte s = 0; s < numBigSquare; s++) {
    x_coord = CORNER_X + ((getBigX(s) - minBigX()) * BIG_SIZE);
    y_coord = CORNER_Y - (((getBigY(s) + 1) - minBigY()) * BIG_SIZE);
    rect(x_coord, y_coord, BIG_SIZE, BIG_SIZE);
  }
  strokeWeight(1);
}

//
// drawGuides
//
// Paints the first few pixels red of each Big Square
// as a way to check orientation
//
void drawGuides() {
  char r = 255;
  char g = 0;
  char b = 0;
  Square s;
  for (byte x = 0; x < pix_width; x++) {
    for (byte y = 0; y < pix_height; y++) {
      if (squareGrid.squareExists(x,y) && squareGrid.getLED(x,y) < 4) {
        squareGrid.setCellColor(color(r,g,b), x, y);  // Simulator
        setPixelBuffer(x, y, r, g, b, false);  // Lights
      }
    }
  }
}

//
//  Server Routines
//
void pollServer() {
  try {
    Client c = _server.available();
    // append any available bytes to the buffer
    if (c != null) {
      _buf.append(c.readString());
    }
    // process as many lines as we can find in the buffer
    int ix = _buf.indexOf("\n");
    while (ix > -1) {
      String msg = _buf.substring(0, ix);
      msg = msg.trim();
      //println(msg);
      processCommand(msg);
      _buf.delete(0, ix+1);
      ix = _buf.indexOf("\n");
    }
  } catch (Exception e) {
    println("exception handling network command");
    e.printStackTrace();
  }  
}

Pattern cmd_pattern = Pattern.compile("^\\s*(\\d+),(\\d+),(\\d+),(\\d+),(\\d+)\\s*$");
Pattern osc_pattern = Pattern.compile("^\\s*(\\w+),(\\w+),(\\d+)\\s*$");

void processCommand(String cmd) {
  if (VIDEO_STATE) return;  // Videos override python shows
  if (cmd.charAt(0) == 'X') {  // Finish the cycle
    finishCycle();
  } else if (cmd.charAt(0) == 'D') {  // Get the delay time
    delay_time = Integer.valueOf(cmd.substring(1, cmd.length())) + 20;  // 20 is a buffer
  } else {  
    processPixelCommand(cmd);  // Pixel command
  }
}

void processPixelCommand(String cmd) {
  Matcher m = cmd_pattern.matcher(cmd);
  if (!m.find()) {
    println("ignoring input!");
    return;
  }
  byte x = Byte.valueOf(m.group(1));
  byte y = Byte.valueOf(m.group(2));
  int r = Integer.valueOf(m.group(3));
  int g = Integer.valueOf(m.group(4));
  int b = Integer.valueOf(m.group(5));
  
  setPixelBuffer(x, y, (char)r, (char)g, (char)b, false); 
//  println(String.format("setting pixel:(%d,%d) to (%d,%d,%d)", x, y, r, g, b));
}

//
//  Routines to interact with the Lights
//

// Send a corrected color to a square pixel on screen and in lights
void sendColorOut(byte x, byte y, char r, char g, char b) {
  if (squareGrid.squareExists(x,y) == false) return;
  
  color correct = colorCorrect(r,g,b);
  
  r = (char)adj_brightness(red(correct));
  g = (char)adj_brightness(green(correct));
  b = (char)adj_brightness(blue(correct));
  
  squareGrid.setCellColor(color(r,g,b), x, y);  // Simulator
  setPixelBuffer(x, y, r, g, b, true);  // Lights: sets next-frame buffer (doesn't turn them on)
}

//
// Finish Cycle
//
// Get ready for the next morph cycle by:
void finishCycle() {
  morph_frame(1.0);
  pushColorBuffer();
  start_time = millis();  // reset the clock
}

//
// Update Morph
//
void update_morph() {
  if (VIDEO_STATE) return;
  if ((last_time - start_time) > delay_time) {
    return;  // Already finished all morphing - waiting for next command 
  }
  last_time = millis();  // update clock
  morph_frame((last_time - start_time) / (float)delay_time); 
}
  
//
//  Fractional morphing between current and next frame - sends data to lights
//
//  fract is an 0.0-1.0 fraction towards the next frame
//
void morph_frame(float fract) {
  char r,g,b;
  
  for (byte x = 0; x < pix_width; x++) {
    for (byte y = 0; y < pix_height; y++) {
      if (hasChanged(x, y)) {
        r = interp(curr_buffer[x][y][0], next_buffer[x][y][0], fract);
        g = interp(curr_buffer[x][y][1], next_buffer[x][y][1], fract);
        b = interp(curr_buffer[x][y][2], next_buffer[x][y][2], fract);
        
        sendColorOut(x, y, r, g, b);  // Update individual light and simulator
      }
    }
  }
  sendDataToLights();  // Turn on all lights
  squareGrid.draw();  // Update screen display
}  

char interp(char a, char b, float fract) {
  return (char)(a + (fract * (b-a)));
}

void sendDataToLights() {
  if (testObserver.hasStrips) {   
    registry.startPushing();
    registry.setExtraDelay(0);
    registry.setAutoThrottle(true);
    registry.setAntiLog(true);    

    byte counter = 0;
    List<Strip> strip_list = registry.getStrips();
    Strip[] strips = new Strip[numBigSquare];
    for (Strip strip : strip_list) {
      if (counter < numBigSquare && counter < strips.length) {
        strips[counter] = strip;
        counter++;
      }
    }
    
    for (byte x = 0; x < pix_width; x++) {
      for (byte y = 0; y < pix_height; y++) {
        if (squareGrid.squareExists(x,y) && hasChanged(x,y)) {
           strips[squareGrid.getStrip(x,y)].setPixel(getPixelBuffer(x,y), squareGrid.getLED(x,y));
        }
      }
    }
  }
}

void movePixelsToBuffer() {
  
  for (byte y = 0; y < pix_height; y++) {  // rows
    for (byte x = 0; x < pix_width; x++) {  // columns
      RGBColor rgb = pixelarray.GetPixelColor(x,y);
      char r = (char)rgb.r;
      char g = (char)rgb.g;
      char b = (char)rgb.b;
      
      sendColorOut(x, y, r, g, b);  // Update individual light and simulator
    }
  }
  sendDataToLights();  // Turn on all lights
  squareGrid.draw();  // Update screen display
}

private void prepareExitHandler () {

  Runtime.getRuntime().addShutdownHook(new Thread(new Runnable() {

    public void run () {

      System.out.println("Shutdown hook running");

      List<Strip> strip_list = registry.getStrips();
      for (Strip strip : strip_list) {
        for (int i=0; i<strip.getLength(); i++)
          strip.setPixel(#000000, i);
      }
      for (int i=0; i<100000; i++)
        Thread.yield();
    }
  }
  ));
}

//
//  Routines for the strip buffer
//

int adj_brightness(float value) {
  return (int)(value * BRIGHTNESS / 100);
}

color colorCorrect(int r, int g, int b) {
  switch(COLOR_STATE) {
    case 1:  // no red
      if (r > 0) {
        if (g == 0) {
          g = r;
          r = 0;
        } else if (b == 0) {
          b = r;
          r = 0;
        }
      }
      break;
    
    case 2:  // no green
      if (g > 0) {
        if (r == 0) {
          r = g;
          g = 0;
        } else if (b == 0) {
          b = g;
          g = 0;
        }
      }
      break;
    
    case 3:  // no blue
      if (b > 0) {
        if (r == 0) {
          r = b;
          b = 0;
        } else if (g == 0) {
          g = b;
          b = 0;
        }
      }
      break;
    
    case 4:  // all red
      if (r == 0) {
        if (g > b) {
          r = g;
          g = 0;
        } else {
          r = b;
          b = 0;
        }
      }
      break;
    
    case 5:  // all green
      if (g == 0) {
        if (r > b) {
          g = r;
          r = 0;
        } else {
          g = b;
          b = 0;
        }
      }
      break;
    
    case 6:  // all blue
      if (b == 0) {
        if (r > g) {
          b = r;
          r = 0;
        } else {
          b = g;
          g = 0;
        }
      }
      break;
    
    default:
      break;
  }
  return color(r,g,b);   
}

void initializeColorBuffers() {
  char empty = 0;
  for (byte x = 0; x < pix_width; x++) {
    for (byte y = 0; y < pix_height; y++) {
      setPixelBuffer(x, y, empty, empty, empty, false);
    }
  }
  pushColorBuffer();
}

void setPixelBuffer(byte x, byte y, char r, char g, char b, boolean morph) {
  if (morph) {
    morph_buffer[x][y][0] = r;
    morph_buffer[x][y][1] = g;
    morph_buffer[x][y][2] = b;
  } else {
    next_buffer[x][y][0] = r;
    next_buffer[x][y][1] = g;
    next_buffer[x][y][2] = b;
  }
}

color getPixelBuffer(byte x, byte y) {
  return color(morph_buffer[x][y][0],
               morph_buffer[x][y][1],
               morph_buffer[x][y][2]);
}

boolean hasChanged(byte x, byte y) {
  return (curr_buffer[x][y][0] != next_buffer[x][y][0] ||
          curr_buffer[x][y][1] != next_buffer[x][y][1] ||
          curr_buffer[x][y][2] != next_buffer[x][y][2]);
}

void pushColorBuffer() {
  for (byte x = 0; x < pix_width; x++) {
    for (byte y = 0; y < pix_height; y++) {
      curr_buffer[x][y][0] = next_buffer[x][y][0];
      curr_buffer[x][y][1] = next_buffer[x][y][1];
      curr_buffer[x][y][2] = next_buffer[x][y][2]; 
    }
  }
}

int bounds(int value, int minimun, int maximum) {
  if (value < minimun) return minimun;
  if (value > maximum) return maximum;
  return value;
}
    
  
  


