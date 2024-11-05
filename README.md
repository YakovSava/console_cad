# What is it?

This is a console CAD, it creates a `dxf` file and is based on Python and the `ezdxf` library, it helps to do everything through the console, but unfortunately it does not allow you to view it

# Usage example:

### Draw a line:
```cad
line (10, 10) (10, 0)
```
Places a line in the coordinates `(10, 10)` with a length of 10 and an angle of inclination of 0 degrees

### Draw a circle

```cad
circle (10, 5) 5
```
Places a circle on the coordinates `(10, 5)` with a radius of 5 (diameter 10, respectively)

### Draw a rectangle
```cad
rectangle (0, 0) (30, 20)
```
Draw a square with a starting point at `(0, 0)`, length 30 and width 20

### Draw a polyline
```cad
polyline (0, 0) (10, 10) (20, 0)
```
1. (0, 0) is the starting point of the polyline.
2. (10, 10) is the second point to which a straight line will be drawn from the starting point (0, 0).
3. (20, 0) — The third point to which a straight line will be drawn from the point (10, 10).

<div align="center">
    That's what we got!
    <img src="https://raw.githubusercontent.com/YakovSava/console_cad/refs/heads/main/readme_example.png">
</div>

## How do I run this?

It's simple!
```shell
git clone https://github.com/YakovSava/console_cad
cd console_cad
make prestart
make start
```

<blockquote>In fact, I wrote this project as a by-product of the course work: to build the layout, I needed at least some kind of CAD, but I have Linux, and I need a convenient two-dimensional CAD, and I did not find anything better than to write my own little console CAD myself rather than suffer than with some kind of LibreCAD which I still don't understand</blockquote>