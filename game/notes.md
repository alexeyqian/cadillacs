

Key snapshot
An input snapshot records the exact state of the controls at a single, frozen millisecond, rather than a history of everything that happened between frames.

An input snapshot is taken at the very beginning of the frame interval.This specific timing ensures that the game engine has the most up-to-date player choices before it runs any game logic, physics updates, or graphics rendering.

The Order of a Game FrameEvery frame in a 2D game follows a strict, linear timeline. It looks like this:Start of Frame → [Take Input Snapshot]: The game grabs the current state of the keyboard, mouse, or controller right now.Process Logic & Physics: The game updates positions. (e.g., Is Jump True in the snapshot? Move the player up.)Render Graphics: The GPU draws the updated positions on the screen.End of Frame → Display: The completed frame is pushed to your monitor.
