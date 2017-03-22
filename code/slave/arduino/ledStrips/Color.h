/*

 A class for color for the tft 1.8" sceens
 color is 16 bit so r, g , and b are 5,6 and 5 bits respectively
*/

#ifndef Color_h
#define Color_h

#if defined(ARDUINO) && ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif


class Color
{
  public:
    Color();
    Color(byte r, byte g, byte b);
    void set_color(byte r, byte g, byte b);
    void set_color_hsb(byte h, byte s, byte b);

    void rgbToHsl(double hsl[]);
    Color multiplyLum(double decrease, double capping);
    static Color hslToRgb(double h, double s, double l);
    byte red;
    byte green;
    byte blue;
    int my_color;
  private:
    void convert_rgb_to_hsb(float r, float g, float b);
    void convert_hcl_to_rgb(float h, float c, float l);
    static double hue2rgb(double p, double q, double t);
    double threeway_max(double a, double b, double c);
    double threeway_min(double a, double b, double c);
};



#endif
