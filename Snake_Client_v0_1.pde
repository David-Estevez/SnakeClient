//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
//-- Snake Client
//------------------------------------------------------------------------------
//-- Let your computer make all the work! This is a simple and quick sketch to
//-- test the basic functionalities of a 2-axis modular robot (i,e: snake) and its
//-- basic movement parameters. 
//--
//-- Future versions will be more complex and will feature more options and movements.
//-- 
//-- For more info, read README.md
//------------------------------------------------------------------------------
//-- Author: 
//-- David Estévez-Fernández, May 2012
//-- GPL license
//------------------------------------------------------------------------------
//-- Requires:
//--
//-- SnakeServer firmware:
//-- https://github.com/David-Estevez/SnakeServer
//-- 
//-- ControlP5 GUI library by Andreas Schlegel, 2012
//-- www.sojamo.de/libraries/controlp5
//------------------------------------------------------------------------------



import controlP5.*;
import processing.serial.*;

ControlP5 cp5;
Serial robot;

StringBuffer command = new StringBuffer();

//-- If you changed your init_key on the firmware you should also change it here:
String init_key = "i1234";

//-- Create some variables that store the current paramenters and the values of the
//-- controls:

int amplitude_X = 0, Amplitude_X = 0;
int phase_X = 0, Phase_X = 0;
int offset_X = 0, Offset_X = 0;

int amplitude_Y = 0, Amplitude_Y = 0;
int phase_Y = 0, Phase_Y = 0;
int offset_Y = 0, Offset_Y = 0;



void setup() {
  //-- Size of the window  
  size(370,250);

  //-- Configuring controls
  cp5 = new ControlP5(this);
  
  Group g1 = cp5.addGroup("ServoX")
                .setPosition(20,20)
                .setWidth(330)
                .activateEvent(true)
                .setBackgroundColor(color(255,80))
                .setBackgroundHeight(80) 
                .setLabel("Snake - X AXIS")
                ;
  
  cp5.addSlider("Amplitude_X")
     .setPosition(20,25)
     .setSize(180,9)
     .setRange(0,90)
     .setGroup(g1)
     ;
     
  cp5.addSlider("Phase_X")
     .setPosition(20,40)
     .setSize(180,9)
     .setRange(-360,360)
     .setSliderMode(Slider.FLEXIBLE)
     .setGroup(g1)
     ;
     
  cp5.addKnob("Offset_X")
               .setRange(-90,90)
               .setValue(0)
               .setPosition(260, 10)
               .setRadius(25)
               .setViewStyle(Knob.ARC)
               .setGroup(g1)
               ;
               

   Group g2 = cp5.addGroup("ServoY")
                .setPosition(20,120)
                .setWidth(330)
                .activateEvent(true)
                .setBackgroundColor(color(255,80))
                .setBackgroundHeight(80) 
                .setLabel("Snake - Y AXIS")
                ;
  
  cp5.addSlider("Amplitude_Y")
     .setPosition(20,25)
     .setSize(180,9)
     .setRange(0,90)
     .setGroup(g2)
     ;
     
  cp5.addSlider("Phase_Y")
     .setPosition(20,40)
     .setSize(180,9)
     .setRange(-360,360)
     .setSliderMode(Slider.FLEXIBLE)
     .setGroup(g2)
     ;
     
  cp5.addKnob("Offset_Y")
               .setRange(-90,90)
               .setValue(0)
               .setPosition(260, 10)
               .setRadius(25)
               .setViewStyle(Knob.ARC)
               .setGroup(g2)
               ;       
                
      //-- Connecting to the robot
      println(Serial.list());
      String portName = Serial.list()[0]; //--By default it selects the first serial port available
      robot = new Serial(this, portName, 9600);
      robot.write( init_key );
}


void draw() {
  
    background(0);
    
    //-- Controls for X axis
    if (amplitude_X != Amplitude_X)
         {
           amplitude_X = Amplitude_X;
           robot.write( "XA" + amplitude_X);
         }
         
    if (offset_X != Offset_X)
         {
           offset_X = Offset_X;
           robot.write( "XO" + offset_X);
         }
         
    if (phase_X != Phase_X)
         {
           /*This works for a head module*/
           int ph = -180;
           phase_X = Phase_X;
           robot.write( "X0P" + ph);
           ph+=180;
           robot.write("X0P" + ph);
           ph+=phase_X;
           robot.write("X1P" + ph);
           ph+=phase_X;
           robot.write("X2P" + ph);
           
         }
         
         
         //-- Controls for Y axis
         if (amplitude_Y != Amplitude_Y)
         {
           amplitude_Y = Amplitude_Y;
           robot.write( "YA" + amplitude_Y);
         }
         
    if (offset_Y != Offset_Y)
         {
           offset_Y = Offset_Y;
           robot.write( "YO" + offset_Y);
         }
         
    if (phase_Y != Phase_Y)
         {
           int ph = 0;
           phase_Y = Phase_Y;
           robot.write( "Y0P" + phase_Y);
         }
}


void controlEvent(ControlEvent theEvent) {
  if(theEvent.isGroup()) {
    println("got an event from group "
            +theEvent.group().name()
            +", isOpen? "+theEvent.group().isOpen()
            );
            
  } else if (theEvent.isController()){
    println("got something from a controller "
            +theEvent.controller().name()
            )
    ;
  }
}


void keyPressed() {
  if(key==' ') {
    cp5.group("g1").remove();
  }
}
