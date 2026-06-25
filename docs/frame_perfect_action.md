### Best Practices for Frame-Perfect Actions in Game Development

Achieving frame-perfect actions requires a strict separation of **hardware polling**, **logic simulation**, and **visual rendering**. If these systems are tangled, frame rate drops will cause inputs to be dropped, eaten, or delayed.

* * *

### 1\. Use Event-Driven Polling (Not State Checks)

*   **The Trap:** Checking `Input.isKeyPressed()` during the snapshot only tells you if the key is down at that exact millisecond. A fast tap between frames gets completely lost.
*   **The Solution:** Use your engine's OS event loop (like `WM_KEYDOWN`, SDL events, or `InputSystem.onActionTriggered`).
*   **The Rule:** The OS event listener must append presses to a **buffer queue** immediately when they happen, independent of the frame rate.

### 2\. Decouple Input from Rendering (Fixed Timesteps)

Never process gameplay logic or input snapshots inside a variable frame rate loop (like Unity's `Update` or Godot's `_process`). If the game drops from 60fps to 30fps, your physics slows down and inputs get sloppy.

*   **The Rule:** Process your input snapshots inside a **Fixed Timestep Loop** (like `FixedUpdate` or `_physics_process`).
*   **The Cadence:** Run this physics loop at a locked interval (usually 60Hz or 120Hz). If a rendering frame takes too long, the game will run multiple fixed loops in a row to catch up, ensuring no input snapshots are skipped.

### 3\. Implement an Input Buffer (Input Queue)

In high-precision games (like fighting games or precision platformers), human players cannot always press a button on the *exact* 16.6ms window required.

*   **The Solution:** Create an **Input Buffer** that remembers actions for a small window of frames (typically 3 to 6 frames, or about 50–100ms).
*   **The Execution:** If a player presses "Jump" 2 frames *before* they actually hit the ground, store `Jump` in the buffer. The instant the player lands, the game checks the buffer, sees the pending jump, and executes it immediately. This feels "frame-perfect" to the player without feeling unresponsive.

### 4\. State-Based Input Consumption

To prevent a single button press from triggering an action multiple times across frames, treat inputs as consumable resources.

*   **The Flow:**
    1.  The Snapshot captures `Jump = True`.
    2.  The Player State Machine processes the jump logic.
    3.  The Player State Machine immediately sets `Jump = Consumed` or clears that specific buffer flag.
    4.  Even if the physics loop checks the snapshot again before the next hardware poll, the jump cannot re-trigger.

### 5\. Eliminate Double-Emitted Actions

When a player taps a button, the hardware can occasionally vibrate, causing the OS to register two incredibly fast presses (button bouncing).

*   **The Practice:** Enforce a tiny cooldown (e.g., 1–2 frames) on discrete actions like menus, dashes, or attacks, unless the game explicitly allows rapid-fire inputs.

* * *

### Standardized 2D Input Snapshot Struct

For high-precision and netcode-ready games, represent your snapshot as a clean, minimal data structure:

cpp

    struct InputSnapshot {
        uint32_t frameNumber;      // The exact game tick this belongs to
        float moveX;               // Directional X (-1.0 to 1.0)
        float moveY;               // Directional Y (-1.0 to 1.0)
        uint8_t actionButtons;     // Bitmask for actions (Bit 0: Jump, Bit 1: Attack, etc.)
    };
    

Use code with caution.

*Using a bitmask for buttons keeps the snapshot incredibly tiny, which is vital if you ever expand your frame-perfect system into multiplayer rollback netcode.*