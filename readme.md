a puzzle-piece generator

### gameplan
* write some function, generate_peninsula, that can draw puzzle piece-ish lines
* generate a grid of vertices - perturb it a bit so it's not perfectly rectangular
* connect neighboring pairs of vertices in segments
* for each segment, pick a random staring vertex
* run spline = generate_peninsula(start, end)
* handle board edges as ..edge cases
