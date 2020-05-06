/*
  Square Simulator Only - draws squares on the monitor
  
  Stripped down simulator to use with the DMX king
  
  No logic: all received (pixel, color) messages are drawn immediately
  
  Colors are hsv, because that's what the Python Showrunner uses
  
  Compatible with Processing 2 + 3
  
  5/5/20
  
*/

// Relative coordinates for the Big Squares
int NUM_BIG_SQUARE = 4;
int[][] BigSquareCoord = {
  {0,0},  // Square 1
  {1,0},  // Square 2
  {2,0},  // Square 3
  {3,0}   // Square 4
};

import processing.net.*;
import java.util.*;
import java.util.regex.*;
import java.awt.Color;

// network vars
int port = 4444;
Server _server; 
StringBuffer _buf;

// How many little squares on the base of each big square
int PIXEL_WIDTH = 12;  // Height & width in pixels (LEDs) of each square
int PIX_WIDTH = (int)(grid_width() * PIXEL_WIDTH);  // x-axis for buffer
int PIX_HEIGHT = (int)(grid_height() * PIXEL_WIDTH);  // y-axis for buffer

// Calculated pixel constants for simulator display
int SCREEN_SIZE = 1200;  // hex screenfloat SMALL_SIZE = (SCREEN_SIZE - 20) / (PIXEL_WIDTH * NUM_HEXES);  // Size of a small hex
float SMALL_SIZE = (SCREEN_SIZE - 20) / (PIXEL_WIDTH * grid_width());  // Size of a small square
int BIG_SIZE = (int)(PIXEL_WIDTH * SMALL_SIZE);  // Width of one big square
int SCREEN_WIDTH = (int)(BIG_SIZE * grid_width()) + 20;  // Width + a little
int SCREEN_HEIGHT = (BIG_SIZE * grid_height()) + 20; // Height + a little
int CORNER_X = 10; // bottom left corner position on the screen
int CORNER_Y = SCREEN_HEIGHT - 10; // bottom left corner position on the screen

int DRAW_LABELS = 2;

SquareForm squareGrid;  // Grid model of Big Squares

//
// Helper classes: Coord
//
class Coord {
  public int x, y;
  
  Coord(int x, int y) {
    this.x = x;
    this.y = y;
  }
}

//
// setup
//
//void settings() {
//  size(SCREEN_WIDTH, SCREEN_HEIGHT);  // Processing 3
//}

void setup() {
  size(SCREEN_WIDTH, SCREEN_HEIGHT);  // Processing 2 (comment out if using 3)
  colorMode(HSB, 255);  // HSB colors (not hsv)
  
  stroke(0);
  fill(0, 0, 128);
  
  frameRate(10);
  
  squareGrid = makeSquareGrid();  // Set up the Big Squares and stuff in the little squares
  
  _buf = new StringBuffer();
  _server = new Server(this, port);
  println("server listening: " + _server);
  
  drawSquares();
}

void draw() {
  // Get (pixel, color) messages from python show runner
  // and draw them as fast as possible
  pollServer();  
}

void drawSquares() {
  squareGrid.draw();  // Draw all squares
  drawBigFrames();     // Draw a bold frame around each grid
}

//
// Get helper functions
//
// Makes code more readable
// No out-of-bounds error handling. Make sure grid# is valid!
int getBigX(int grid) { return (BigSquareCoord[grid][0]); }
int getBigY(int grid) { return (BigSquareCoord[grid][1]); }

//
// minBigX
//
// Smallest BigX value
int minBigX() {
  int min_x = getBigX(0);
  for (int i = 1; i < NUM_BIG_SQUARE; i++) {
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
  for (int i = 1; i < NUM_BIG_SQUARE; i++) {
    if (getBigY(i) < min_y) min_y = getBigY(i);
  }
  return min_y;
}

//
// grid_width
//
// How many squares across is the big grid?
float grid_width() {
  int min_x = getBigX(0);
  int max_x = min_x;
  int new_x;
  
  for (int i=1; i < NUM_BIG_SQUARE; i++) {
    new_x = getBigX(i);
    if (new_x < min_x) { min_x = new_x; }
    if (new_x > max_x) { max_x = new_x; }
  }
  return (max_x - min_x + 1);
}

//
// grid_height
//
// How many squares high is the big grid?
int grid_height() {
  int min_y = getBigY(0);
  int max_y = min_y;
  int new_y;
  
  for (int i=1; i < NUM_BIG_SQUARE; i++) {
    new_y = getBigY(i);
    if (new_y < min_y) { min_y = new_y; }
    if (new_y > max_y) { max_y = new_y; }
  }
  return (max_y - min_y + 1);
}


//
// SquareForm class holds an 2D-array of Squares (another class) 
//
SquareForm makeSquareGrid() {
  float pix_x, pix_y;
  
  SquareForm form = new SquareForm(PIX_WIDTH, PIX_HEIGHT);
  
  for (int i = 0; i < NUM_BIG_SQUARE; i++) {
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
        Square square = new Square(pix_x, pix_y, x + x_offset, y + y_offset, i);
        form.add(square, x + x_offset, y + y_offset);
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
  
  void draw() {
    for (byte x = 0; x < this.x_width; x++) {
      for (byte y = 0; y < this.y_height; y++) {
        if (squareExists(x,y)) {
          this.squares[x][y].draw();
        }
      }
    }
  }
  
  void setCellColor(int c, byte x, byte y) {
    this.squares[x][y].setColor(c);
  }
  
  boolean squareExists(byte x, byte y) {
    return (InBounds(x, y) && this.squares[x][y] != null);
  }
}

//
//  Square shape primitives
//
class Square {
  String id = null; // "xcoord, ycoord"
  int x;  // x in the square array
  int y;  // y in the square array
  float pix_x;  // x-coordinate in pixels on the screen
  float pix_y;  // y-coordinate in pixels on the screen
  int strip; // strip number
  int LED;     // LED number on the strand
  int c;  // color
  
  Square(float pix_x, float pix_y, int x, int y, int strip) {
    this.x = x;
    this.y = y;
    this.pix_x = pix_x;
    this.pix_y = pix_y;
    this.strip = strip;
    this.LED = 0;
    this.c = get_hsv_color(0, 0, 255);
    
    int[] coords = new int[2];
    coords[0] = x;
    coords[1] = y;
    this.id = join(nf(coords, 0), ",");
  }
  
  void setColor(int c) {
    this.c = c;
  }
   
  void draw() {
    fill(get_hue(this.c), get_sat(this.c), get_val(this.c));
    stroke(0);
    rect(this.pix_x, this.pix_y, SMALL_SIZE, SMALL_SIZE);

//    println("Drawing!" + this.x + " " + this.y + " " + get_hue(this.c) + " " + get_sat(this.c) + " " + get_val(this.c));
//    println("At " + this.pix_x + " " + this.pix_y);
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
// drawBigFrames - Draws a big bold square around each grid
//
void drawBigFrames() {
  noFill();
  strokeWeight(5);
  int x_coord, y_coord;
  
  for (byte s = 0; s < NUM_BIG_SQUARE; s++) {
    x_coord = CORNER_X + ((getBigX(s) - minBigX()) * BIG_SIZE);
    y_coord = CORNER_Y - (((getBigY(s) + 1) - minBigY()) * BIG_SIZE);
    rect(x_coord, y_coord, BIG_SIZE, BIG_SIZE);
  }
  strokeWeight(1);
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
      processCommand(msg);
      _buf.delete(0, ix+1);
      ix = _buf.indexOf("\n");
    }
  } catch (Exception e) {
    println("exception handling network command");
    e.printStackTrace();
  }
}

//
// processCommand
//
// 3 comma-separated numbers for x, y, color
//
Pattern cmd_pattern = Pattern.compile("^\\s*(\\d+),(\\d+),(\\d+)\\s*$");

void processCommand(String cmd) {
  if (cmd.length() < 2) { return; }  // Discard erroneous stub characters
  Matcher m = cmd_pattern.matcher(cmd);
  if (!m.find()) {
    //println(cmd);
    println("ignoring input for " + cmd);
    return;
  }
  byte x  =    Byte.valueOf(m.group(1));
  byte y  =    Byte.valueOf(m.group(2));
  int hsv = Integer.valueOf(m.group(3));
  
  if (squareGrid.squareExists(x,y)) {
    squareGrid.setCellColor(hsv, x, y);
    squareGrid.squares[x][y].draw();
  }
          
//  println(String.format("setting coord:%d,%d to h:%d, s:%d, v:%d", x, y, get_hue(hsv), get_sat(hsv), get_val(hsv)));
}


int get_hsv_color(int h, int s, int v) {
  return h << 16 | s << 8 | v;
}

short get_hue(int c) {
  return (short)(c >> 16 & 0xFF);
}

short get_sat(int c) {
  return (short)(c >> 8 & 0xFF);
}

short get_val(int c) {
  return (short)(c & 0xFF);
}

void print_memory_usage() {
  long maxMemory = Runtime.getRuntime().maxMemory();
  long allocatedMemory = Runtime.getRuntime().totalMemory();
  long freeMemory = Runtime.getRuntime().freeMemory();
  int inUseMb = int(allocatedMemory / 1000000);
  
  if (inUseMb > 80) {
    println("Memory in use: " + inUseMb + "Mb");
  }  
}
