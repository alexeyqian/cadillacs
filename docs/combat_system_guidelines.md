# 2D Beat 'Em Up Combat System Design Guidelines
*Engineering and Design Blueprint for Variable Frame & Collision Architecture*

---

## 1. Core Sprite Architecture & Variable Frame Handling
In 2D combat development, forcing animation frames into fixed bounding boxes wastes video memory (Overdraw) and hinders performance. Best practice dictates using tightly trimmed, variable frame sizes managed via external offset maps.

### The Fixed Ground Anchor Rule
*   **The Problem:** Aligning variable frames by their top-left corner or visual center causes characters to violently jitter, teleport, or "ice-skate" across the floor during animation transitions.
*   **The Solution:** Establish an unchanging **Ground Pivot Anchor Node `(0, 0)`** located on the floor, precisely centered between the character's feet.
*   **Implementation:** Let the visual image boundaries expand irregularly around this point. Every individual animation frame must be paired with an `offset_x` and `offset_y` tuple representing the distance from the Ground Pivot to the frame surface's top-left corner.

---

## 2. Dynamic Collision Layer System (The Multi-Box Paradigm)
Never map game logic directly to visual sprite dimensions. Combat execution requires separating rendering surfaces into three independent, non-rotating geometric layers (`pygame.Rect`).

### Layer 1: Ground Base Box (`base_rect`)
*   **Purpose:** Handles environmental terrain collisions, wall boundaries, and screen constraints.
*   **Design:** A tiny, stable horizontal rectangle anchored directly over the ground pivot. It must remain identical across almost all animations (e.g., Idle, Punch, Walk) to keep movement mechanics perfectly stable.

### Layer 2: Vulnerable Area Box (`hurtbox`)
*   **Purpose:** Processes incoming enemy damage, projectiles, and environmental hazards.
*   **Design (The Multi-Box Solution):** Standard rectangles cannot rotate. Wrapping a diagonal extended limb or a complex human shape inside *one single* box creates wide corners of empty air, causing frustrating "ghost hits." 
*   **Best Practice:** Layer multiple, tightly stacked rectangles (e.g., separate Head, Torso, and Leg boxes) to cleanly trace a character's posture without capturing blank space. Movement sequences (Walk/Run) should use a simplified, centered vertical column covering the legs to keep tracking predictable.

### Layer 3: Strike Zone Box (`attack_hitbox`)
*   **Purpose:** Triggers damage regions during offensive frame states.
*   **Design:** To enforce honest, precise visual design, the attack hitbox must never capture the entire arm or leg. Wrap the hitbox tightly around **only the striking component (the fist or the boot)** plus 10–15 pixels of the forearm/shin. Leaving the shoulder and bicep as a green hurtbox keeps extended limbs vulnerable to strategic counter-attacks.

---

## 3. Combat Timeline Flow (Animation Phases)
Every melee strike action must be sequenced into three distinct phases across the game logic loop:

1.  **Startup / Wind-up:** The character draws back their arm/leg. **No attack hitbox is generated.**
2.  **Active Strike:** The limb fully extends. **The precise attack hitbox is activated.** This is the only phase capable of running collision logic checks against enemy hurtboxes.
3.  **Recovery / Followthrough:** The character retracts the limb back to their base stance. **The attack hitbox is instantly deleted/disabled.**

---

## 4. Advanced Interaction & Game Logic Integrity

### Prevent the "Machine-Gun" Multi-Hit Bug
If an attack hitbox stays active across 3 sequential frames, a basic collision loop will apply damage 3 times instantly, melting enemy health bars. 
*   **The Solution:** Implement a **Hit Memory Cache** array unique to the attack instance. The moment a strike connects, store the victim's unique ID in the cache. As long as that ID rests in the cache, the active hitbox passes through them harmlessly. Wipe the cache only when the player exits the attack sequence or triggers a fresh move.
*   **True Multi-Hits:** For intentional multi-strike moves (e.g., spinning moves), explicitly execute a `.clear()` on the memory cache at specific animation keyframes to allow a second valid hit registration.

### Counter-Hit Logic
*   **Rule:** When a character extends a strike, their limb hurtbox stretches forward alongside the attack hitbox.
*   **Check Routine:** Test for enemy attacks striking the player's extended limb *before* evaluating the player's own forward strike box. If an enemy hits the extended arm hurtbox during its startup or active window, trigger a Counter-Hit. This cancels the player's attack frames, overrides their input, and drops them into a prolonged hit-stun state.

### Hitbox Clashing (Deflection & Parries)
When two opposing red attack hitboxes intersect on the exact same frame before touching a green body hurtbox:
1.  **Weapon/Fist Deflection:** Override standard damage processing and exit the combat loop immediately.
2.  **State Recoil:** Clear out both attack hitboxes and shift both characters into a brief, unique "Recoil" animation phase.
3.  **Physics Reflection:** Apply a small, matching backward velocity vector to pop both characters apart safely.

---

## 5. Development Summary Checklist
*   [ ] **Separate rendering from logic:** Sprites change width/height constantly; world vectors, hitboxes, and footprints remain absolute.
*   [ ] **Anchor to the floor:** Pin the character's world position to a single tracking spot on the ground (`world_x, world_y`).
*   [ ] **Utilize multi-box structures:** Stack small rectangles along complex physical frames to eliminate empty corner space.
*   [ ] **Isolate strikes:** Hitboxes belong exclusively on hitting tools (fists, boots, blades), not the shoulder or torso.
*   [ ] **Implement a hit cache:** Protect your engine from machine-gun damage loops by saving struck entity IDs.
*   [ ] **Build a Debug Overlay:** Bind a developer key (e.g., `F1`) to draw your rects (`base_rect` in blue, `hurtbox` in green, `hitbox` in red) dynamically over your artwork to inspect alignments in real-time.
