# Scratch — A Complete Beginner's Guide for Children

- **Document ID:** KB-SCRATCH-18
- **Status:** general educational guide for children, parents and teachers
- **Applies to:** Scratch 3, beginner coding, creative projects and classroom activities
- **Keywords:** Scratch, block programming, coding for kids, children, animation, game, sprite, stage, event, loop, variable, broadcast, debugging, ohjelmointi lapsille

## 1. What is Scratch?

Scratch is a visual programming environment. You make programs by connecting colorful blocks instead of typing lots of code. You can create stories, animations, games, music and interactive art.

The main idea is simple: **choose a character, connect blocks, press the green flag and see what happens.**

Use the official Scratch website or an approved offline editor. Ask a parent or teacher before creating an account or sharing a project publicly.

## 2. Meet the Scratch workspace

- **Stage:** the area where your project happens.
- **Sprite:** a character or object that can move and react.
- **Backdrop:** the stage's background.
- **Blocks palette:** the available coding blocks, grouped by color/category.
- **Code area:** where you connect blocks.
- **Green flag:** starts scripts that use the green-flag event.
- **Stop button:** stops running scripts.
- **Costumes:** different looks for a sprite.
- **Sounds:** audio a sprite can play.

## 3. Your first animation

1. Open a new project.
2. Choose a sprite, such as a cat.
3. Add an Events block: **when green flag clicked**.
4. Add Motion: **move 10 steps**.
5. Add Looks: **say Hello! for 2 seconds**.
6. Press the green flag.

Change the number of steps and the message. Notice how the result changes.

## 4. The main block families

| Category | What it does | Example idea |
|---|---|---|
| Motion | Moves and turns sprites | Walk across the stage |
| Looks | Changes costume, size, visibility or speech bubble | Make a character talk |
| Sound | Plays sounds and music | Add a jump sound |
| Events | Starts scripts when something happens | Green flag or key pressed |
| Control | Repeats, waits and makes decisions | Repeat a dance |
| Sensing | Detects keys, mouse, touching and more | Detect a wall |
| Operators | Math and logic | Add score or compare values |
| Variables | Stores changing information | Score and lives |
| My Blocks | Creates reusable custom blocks | Make a jump command |

Block names may vary slightly with language and Scratch version.

## 5. Events: when should the program start?

Events are triggers. Examples:
- when green flag clicked;
- when a key is pressed;
- when this sprite clicked;
- when I receive a message.

A script normally begins with an event block. Different sprites can run different scripts at the same time.

## 6. Sequences and loops

A sequence runs blocks in order, from top to bottom.

A loop repeats instructions:
- `repeat 10`: repeat a fixed number of times;
- `forever`: keep repeating until the project is stopped;
- `repeat until`: repeat while waiting for a condition to become true.

Try a dance: repeat 8 times, move 20 steps, turn 45 degrees, wait a short time.

## 7. Decisions: if and if/else

A decision checks a condition.

Example idea:
- If the sprite touches the edge, turn around.
- If the answer is correct, say “Great job!”
- Otherwise, ask the question again.

Conditions can use sensing blocks and comparison operators such as equals, greater than and less than.

## 8. Variables: remember information

A variable is a named box that stores a value.

Create a variable called `score`:
1. Set score to 0 when the game starts.
2. When the player catches an object, change score by 1.
3. Display the score on the stage.

Use variables for score, timer, lives, speed and level. Decide which sprite or scripts need access to each variable.

## 9. Messages and multiple sprites

Broadcast messages let sprites coordinate.

Example:
1. The player touches the goal.
2. The player broadcasts `level complete`.
3. The stage or another sprite receives that message.
4. The receiver changes the backdrop or shows a celebration.

Use clear message names. Avoid sending the same message repeatedly in a fast forever loop unless that is intended.

## 10. Make a simple catching game

**Goal:** move a basket left and right to catch falling fruit.

1. Choose a basket sprite and a fruit sprite.
2. Use left/right arrow key events to move the basket.
3. Place the fruit near the top.
4. Make the fruit fall repeatedly.
5. If fruit touches basket: increase score and return fruit to the top.
6. If fruit reaches the bottom: reduce a life or restart its position.
7. Add a timer or winning score.
8. Test with different speeds.

Build one feature at a time. First make movement work, then falling, then collision, then score.

## 11. Debugging: become a program detective

When something does not work:
1. Press stop.
2. Check that the correct sprite is selected.
3. Check that the script starts with the intended event.
4. Read blocks from top to bottom.
5. Look for a forever loop that never waits.
6. Check variable names and starting values.
7. Test one change at a time.
8. Ask: “What did I expect? What happened instead?”

A bug is not failure. It is a clue that helps you understand your program.

## 12. Creative project ideas

- Animated greeting card.
- A story with two characters and a conversation.
- Maze game with arrow keys.
- Quiz with score.
- Musical instrument controlled by keys.
- Drawing tool using the pen extension.
- Platform game with levels.
- Interactive science or maths demonstration.

Choose an idea you enjoy. Draw a plan before coding: characters, goal, controls, rules and how the project ends.

## 13. Online safety for children

- Ask a trusted adult before making an account or sharing a project.
- Do not publish your real name, home address, school, phone number, passwords or private photos.
- Do not chat with strangers or follow links from unknown people.
- Tell a trusted adult if something online feels uncomfortable.
- Be kind when commenting on other people's projects.
- Use music and images you made yourself or are allowed to use.
- A parent or teacher should review privacy and sharing settings.

## 14. Learning path

1. Events and simple sequences.
2. Motion, looks and sounds.
3. Loops and waits.
4. If/else and sensing.
5. Variables and score.
6. Broadcast messages and multiple sprites.
7. Clone and custom blocks.
8. Plan, build, test and explain a complete game.

## 15. Teaching approach

For younger learners, explain one new idea at a time. Let the child predict what a block will do before running it. Encourage changing one value and observing the result. Celebrate experiments and debugging, not only finished games. Avoid giving a complete solution immediately; use hints and questions so the child can discover the logic.


## Tiivistelmä suomeksi lapsille

Scratchissa ohjelma rakennetaan liittämällä värikkäitä lohkoja toisiinsa. Hahmoa kutsutaan spriteksi ja tausta-aluetta näyttämöksi. Vihreä lippu käynnistää ohjelman. Toisto-lohkot tekevät samoja asioita monta kertaa, ehtolohkot valitsevat mitä tehdään eri tilanteissa ja muuttujat muistavat esimerkiksi pisteet. Kun peli ei toimi, kokeile yhtä lohkoa kerrallaan ja pyydä aikuiselta apua verkon turvallisuuteen.
