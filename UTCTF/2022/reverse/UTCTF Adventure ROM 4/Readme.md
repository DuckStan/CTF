# UTCTF Adventure ROM 4 write-up by Duck Stan ( the first write-up ever ;) )

## Pre-requisites
  **I strongly suggest watching these videos to better understand the Nintendo ROM architecture.**
  - https://www.youtube.com/watch?v=dQLp5i8oS3Y&t=539s&ab_channel=stacksmashing
  - https://www.youtube.com/watch?v=p8OBktd42GI&ab_channel=LiveOverflow
  
  **In order to debug and reverse the binary, use these tools( make sure your Ghidra and GhidraBoy plugin versions match!!!):**
  - https://ghidra-sre.org/
  - https://github.com/Gekkio/GhidraBoy
  - https://sameboy.github.io/
  
  **In order to understand the commands and register/memory purpose use this documentation**
  - https://gbdev.io/pandocs/
  
  **In order to patch our binary, you will need this script**
  - https://github.com/ghidraninja/ghidra_scripts/blob/master/export_gameboy_rom.py

##  Let's Play
  In order to be effective at reversing, it is better to look at the program first. In that case, we have to play this game( and try to complete if we can).
  
  Use the SameBoy emulator to open the game and have some fun!
  
  Basically, you will see something like these:
  
  ![image](https://user-images.githubusercontent.com/25302752/158181244-dd647da2-da21-4b4c-aaeb-78637ebc1b47.png)
  
  ![image](https://user-images.githubusercontent.com/25302752/158181417-739780ac-5bc2-49f4-a678-3cc7b8793dcb.png)

  If you fall down( or fly up??), you will get a bunch of text and a restart:
  
  ![image](https://user-images.githubusercontent.com/25302752/158181166-e72cae8c-eab2-4936-b894-4b21a7fa28ed.png)
  
  Alright, so what if we win? 🥇
  
  ![image](https://user-images.githubusercontent.com/25302752/158182081-20ade1bf-f4d1-49ca-ab0a-1cb962e37c7d.png)
  
  Doesn't look like a win to me 😧
  
  Ok, let's go the hard way and see what's inside by using GhidraBoy plugin:
  
  ![image](https://user-images.githubusercontent.com/25302752/158187035-e74a797d-4621-4362-871f-99816e391e29.png)

  Alright, there is an entry function, and it calls out some FUN_ functions with different arguments. 
  
  Let's try to keep calm and not get overwhelmed by all the commands and operations done in this game. Our goal is to get an understanding of where the game starts for now.
  
  What is in the FUN_0da4()?
  
  ```
  byte FUN_0da4(void)

{
  byte bVar1;
  
  bVar1 = read_volatile_1(LCDC);
  if (CARRY1(bVar1,bVar1) == false) {
    return bVar1 * '\x02';
  }
  do {
    bVar1 = read_volatile_1(LY);
  } while (0x91 < bVar1);
  do {
    bVar1 = read_volatile_1(LY);
  } while (bVar1 < 0x91);
  bVar1 = read_volatile_1(LCDC);
  write_volatile_1(LCDC,bVar1 & 0x7f);
  return bVar1 & 0x7f;
}
```
Yeah, nothing comprehensible again XD However, we can grab an idea by looking at the developers documentation.

Let's see what LCDC, LY means:

![image](https://user-images.githubusercontent.com/25302752/158189452-13b5b711-207f-4451-b18f-ef639970f555.png)

![image](https://user-images.githubusercontent.com/25302752/158189969-9bee48ca-d8cd-4011-8307-9ecf8063e511.png)

Ok, so there is some rendering done. Kind gives us some ideas:
- Maybe we could modify LCDC value to change the output on the screen?
- Could there be a hidden background, or maybe the flag is of the background color??

In order to change the value of LCDC, we should seek for the function write_volatile_1(LCDC...).

And there are some in entry function!

void entry(undefined param_1,undefined param_2)
```
{
  undefined uVar1;
  undefined extraout_D;
  
  IME(0);
  DAT_dffe = 0x15f;
  uVar1 = rst28(0,&DAT_c000,-0x60);
  DAT_dffe = 0x165;
  rst28(uVar1,&DAT_c784,'\x18');
  DAT_dffe = 0x16c;
  DAT_c784 = extraout_D;
  FUN_0da4();
  write_volatile_1(SCY,0);
  write_volatile_1(SCX,0);
  write_volatile_1(STAT,0);
  write_volatile_1(WY,0);
  write_volatile_1(WX,0xa6);
  DAT_dffe = 0x182;
  rst30(FUN_ff80,'\n',&UNK_01c4);
  DAT_dffe = 0x185;
  FUN_ff80();
  DAT_dffe = 0x18b;
  FUN_0d87(0x9c);
  write_volatile_1(BGP,0xe4); // all these are responsible for shades
  write_volatile_1(OBP0,0xe4);
  write_volatile_1(OBP1,0x1b);
  write_volatile_1(LCDC,0xc0); //<-- LCDC is changed
  write_volatile_1(IF,0);
  write_volatile_1(IE,1);
  DAT_ff90 = 1;
  DAT_c786 = 0;
  DAT_c787 = 0;
  write_volatile_1(NR52,0);
  DAT_dffe = 0x1ad;
  FUN_15bc();
  IME(1);
  DAT_dffe = 0x1b1;
  FUN_06b9(); <---- look here!
  do {
    halt();
  } while( true );
}
```
The SCY, WY, WX - all of these work with display coordinates. IF, IE are responsible for enabling triggers in CPU( enable execution of code). 

Let's change LCDC's value. See what happens by patching the instruction with different values( the way of doing so is shown in the attached video).

![image](https://user-images.githubusercontent.com/25302752/158196358-d43dadba-8da9-4d8c-8183-28de5f01a564.png)

Well, nothing changed( at least during the game). Sometimes I managed to make everything besided our player sprite invisible, but it all doesnt get us closer to the flag.

Ok, let's seek the portion where the text with game description is displayed on the screen.

After looking at the insides of every function, you will eventually figure out that we were looking for FUN_06b9(). In order to make things simple, let's rename this function to start_game():

```
  void start_game(void)
{
  undefined2 uVar1;
  byte extraout_E;
  byte bVar2;
  byte extraout_E_00;
  byte extraout_E_01;
  
  uVar1 = output(" \n UTCTF ROM 4\n BY GG\n\n NOW WITH MUSIC\n\nPRESS START TO BEGIN"); // <-------------- this is our output! ( actually FUN_0dd1)
  bVar2 = extraout_E;
  while( true ) {
    read_input(); // <-- button pressing is read via P1 JoyPad input
    if ((bool)(bVar2 >> 7)) break;
    DAT_c0c3 = DAT_c0c3 + '\x01';
    if ((char)((DAT_c0c3 == '\0') << 7) < '\0') {
      DAT_c0c4 = DAT_c0c4 + '\x01';
    }
  }
  uVar1 = FUN_0ded(DAT_c0c3,DAT_c0c3,(char)uVar1,bVar2,DAT_c0c3,DAT_c0c4);
  FUN_0641(uVar1);
  bVar2 = extraout_E_00;
  do {
    DAT_c0c3 = DAT_c0c3 + '\x01';
    if ((char)((DAT_c0c3 == '\0') << 7) < '\0') {
      DAT_c0c4 = DAT_c0c4 + '\x01';
    }
    FUN_0545(bVar2);
    FUN_0875(bVar2);
    FUN_06f0(); <--- this is where entry is called for the second time
    FUN_0d95();
    bVar2 = extraout_E_01;
  } while( true );
}
```
Alright, we now know where this text message is displayed! The first idea that comes to mind - can we output the flag that is hidden somewhere in memory? Let's first try to output anything besides this message.

```
                             *************************************************************
                             *                                                            
                             *  FUNCTION                                                  
                             *************************************************************
                             undefined  __asm  start_game (void )
             undefined         A:1            <RETURN>
                             start_game                                      XREF[1]:     entry_2:01ae (c)   
            06b9 21  f8  06       LD         HL,0x6f8
            06bc e5              PUSH       HL=>s__UTCTF_ROM_4_BY_GG_NOW_WITH_MUSI_06f8      = " \n UTCTF ROM 4\n BY GG\n\n N
            06bd cd  d1  0d       CALL       output_shit                                      undefined output_shit(char * par
            06c0 e8  02           ADD        SP,0x2
```
Hmm, so our output message is pushed onto the stack. We can patch it witn another address. Let's say it will be c0c3, since it is manipulated in our start_game function.

![image](https://user-images.githubusercontent.com/25302752/158200587-ba72883b-e80d-434a-8140-3cd74abc10a4.png)

Yeah! We can output something on the screen and we can control the adress. Sadly, I didn't find flag on any of the adresses, laying there as a plain string. It is possible that other solutions have found a use for this, so make sure to check out other wu's!

Let's look back on our start_game function. I have figured that the first while cycle reads user input(pressed buttons). We can suggest that it waits for the START button to be pressed. 

By looking at all the other functions we can suggest that there are some preparations done(you can see it by placing breakpoints in SameBoy debugger). The one that is different is FUN_06f0(). To reveal the meaning of this function let's call it start_recursion():
```
void start_recursion(void)

{
  byte bVar1;
  byte bVar2;
  byte bVar3;
  char cVar4;
  byte bVar5;
  byte bVar6;
  byte bVar7;
  byte bVar8;
  char cVar10;
  short sVar9;
  ushort local_6;
  ushort local_4;
  ushort local_2;
  
  if ((DAT_c0a1 & 0x80) != 0 || (DAT_c0a1 < 3 || (byte)(DAT_c0a1 - 3) < (DAT_c0a0 < 0xe8))) {
    DAT_c0a1 = DAT_c0a1 + (0xf5 < DAT_c0a0);
    DAT_c0a0 = DAT_c0a0 + 10;
  }
  if ((_DAT_c0a2 & 0x8000) == 0 && (DAT_c0a3 != '\0' || (byte)-DAT_c0a3 < (DAT_c0a2 != 0))) {
    _DAT_c0a2 = CONCAT11(DAT_c0a3 + -1 + (9 < DAT_c0a2),DAT_c0a2 - 10);
  }
  else if ((_DAT_c0a2 & 0x8000) != 0) {
    _DAT_c0a2 = CONCAT11(DAT_c0a3 + (0xf5 < DAT_c0a2),DAT_c0a2 + 10);
  }
  DAT_c0ab = DAT_c0a6 + DAT_c0a0;
  DAT_c0ac = DAT_c0a7 + DAT_c0a1 + CARRY1(DAT_c0a6,DAT_c0a0);
  bVar6 = (byte)_DAT_c0a2;
  DAT_c0a9 = DAT_c0a4 + bVar6;
  cVar10 = (char)(_DAT_c0a2 >> 8);
  DAT_c0aa = DAT_c0a5 + cVar10 + CARRY1(DAT_c0a4,bVar6);
  bVar3 = (DAT_c0ac >> 4) << 1 | (byte)(DAT_c0ac * '\x10') >> 7;
  bVar1 = (DAT_c0a7 >> 4) << 1 | (byte)(DAT_c0a7 << 4) >> 7;
  local_4 = (ushort)bVar1;
  bVar5 = (byte)(DAT_c0a5 << 4) >> 7;
  bVar8 = (DAT_c0a5 >> 4) << 1;
  bVar2 = bVar8 | bVar5;
  local_2 = (ushort)bVar2;
  if (((bVar1 != bVar3) &&
      ((DAT_c0a1 & 0x80) == 0 && (DAT_c0a1 != 0 || (byte)-DAT_c0a1 < (DAT_c0a0 != 0)))) &&
     (bVar3 < 0x13)) {
    sVar9 = CONCAT11(DAT_c1c8,DAT_c1c7) + (ushort)bVar1 * 4 + local_4;
    bVar7 = (byte)(local_2 - 1);
    bVar3 = (byte)(local_2 - 1 >> 8);
    bVar3 = *(byte *)(sVar9 + CONCAT11(bVar3 >> 2,
                                       (byte)(bVar7 >> 1 | bVar3 << 7) >> 1 | (bVar3 >> 1) << 7));
    cVar4 = (bVar7 & 3) * '\x02' + '\x01';
    while (cVar4 = cVar4 + -1, cVar4 != '\0') {
      bVar3 = bVar3 >> 1;
    }
    if ((bVar3 & 3) != 1) {
      bVar3 = *(byte *)(sVar9 + (ushort)(DAT_c0a5 >> 5));
      cVar4 = (bVar8 & 3 | bVar5) * '\x02' + '\x01';
      while (cVar4 = cVar4 + -1, cVar4 != '\0') {
        bVar3 = bVar3 >> 1;
      }
      if ((bVar3 & 3) != 1) goto LAB_03b5;
    }
    DAT_c0a0 = 0;
    DAT_c0a1 = 0;
    sVar9 = (ushort)(byte)(bVar1 << 3) * 0x100 + 0x7ff;
    DAT_c0ab = (char)sVar9;
    DAT_c0ac = (byte)((ushort)sVar9 >> 8);
    DAT_c0a8 = 1;
  }
LAB_03b5:
  bVar5 = (byte)(DAT_c0aa * '\x10') >> 7;
  bVar8 = (DAT_c0aa >> 4) << 1;
  bVar3 = bVar8 | bVar5;
  local_6 = (ushort)bVar3;
  if (bVar2 != bVar3) {
    sVar9 = local_4 - 1;
    local_4 = (ushort)(byte)(bVar2 << 3) * 0x100;
    sVar9 = CONCAT11(DAT_c1c8,DAT_c1c7) + sVar9 * 5;
    if ((_DAT_c0a2 & 0x8000) == 0 && (cVar10 != '\0' || (byte)-cVar10 < (bVar6 != 0))) {
      if (bVar3 < 0x14) {
        bVar3 = *(byte *)(sVar9 + (ushort)(DAT_c0aa >> 5));
        cVar10 = (bVar8 & 3 | bVar5) * '\x02' + '\x01';
        while (cVar10 = cVar10 + -1, cVar10 != '\0') {
          bVar3 = bVar3 >> 1;
        }
        if ((bVar3 & 3) == 1) {
          _DAT_c0a2 = 0;
          DAT_c0a9 = -1;
          DAT_c0aa = (byte)(local_4 + 0x700 >> 8);
        }
      }
    }
    else if (((_DAT_c0a2 & 0x8000) != 0) && (1 < bVar3)) {
      bVar8 = (byte)(local_6 - 1);
      bVar5 = (byte)(local_6 - 1 >> 8);
      bVar5 = *(byte *)(sVar9 + CONCAT11(bVar5 >> 2,
                                         (byte)(bVar8 >> 1 | bVar5 << 7) >> 1 | (bVar5 >> 1) << 7)) ;
      cVar10 = (bVar8 & 3) * '\x02' + '\x01';
      while (cVar10 = cVar10 + -1, cVar10 != '\0') {
        bVar5 = bVar5 >> 1;
      }
      if ((bVar5 & 3) == 1) {
        _DAT_c0a2 = 0;
        DAT_c0a9 = '\x01';
        DAT_c0aa = (byte)(local_4 >> 8);
      }
    }
  }
  if (0xa0 < DAT_c0aa || (byte)(0xa0 - DAT_c0aa) < (DAT_c0a9 != '\0')) { // GO RIGHT
    DAT_c0a9 = '\0';
    DAT_c0aa = 0x20;
    FUN_07cc(1); //    ;)  interesting function as well
  }
  if (DAT_c0aa < 8) { // GO LEFT
    DAT_c0a9 = '\0';
    DAT_c0aa = 0xa0;
    FUN_07cc(0xff);
  }
  DAT_c0a4 = DAT_c0a9;
  DAT_c0a5 = DAT_c0aa;
  DAT_c0a6 = DAT_c0ab;
  DAT_c0a7 = DAT_c0ac;
  if (0xa0 < DAT_c0ac || (byte)(0xa0 - DAT_c0ac) < (DAT_c0ab != '\0')) { // YOU FEEELLLLLLLLLLLLLLL or did YOU RISEEEE UPPP???
    FUN_0150(); // <---- RECURSION!!!!!
  }
  DAT_c000 = DAT_c0a7;
  DAT_c001 = DAT_c0a5;
  return;
}
```
🧟 - that is what most of the people experince when seeing that much of code. However, it is where our solution lies!!!!

Here is an assumption: here we have a pile of code that analyzes player movement, and also draws the map. 

If we look at the FUN_150() function, we will notice that it is the exact copy of entry() functin, but just on another adress. Alright, so this is our recursion starts, but when is it started? Ofc when we fall down or go up!

Soooo, that if statement checks whether we are trying to die by jumping out of the map. What if we change the FUN_0150 function to start_recursion() by patching??

![fake_immortality](https://user-images.githubusercontent.com/25302752/158217351-d0bb56ea-a5f8-48d9-9ba9-e5a992cfc9ff.gif)

IMMORTALTIY!!!!!

Still no flag though, but we now understand that we can jump out of this map by changing the function address in if statements of start_recursion().

There is a really interesting function FUN_07cc() in other if statements. Let's try to call it.

![teleport](https://user-images.githubusercontent.com/25302752/158217786-2eedcac6-11ee-4044-b84d-43e5d246ce3d.gif)

Ok, so we just start teleporting to some places. Have you noticed something odd?? 

![image](https://user-images.githubusercontent.com/25302752/158212329-43b15b4f-8087-4139-ac38-3c275422b9af.png)

I have once stopped on this level, and have figured that there is probably a level with textures that show the flag!

There is one problem left: how do we get there normally without teleporting?

Let's take a closer look at these statements in start_recursion():
```
if (0xa0 < DAT_c0aa || (byte)(0xa0 - DAT_c0aa) < (DAT_c0a9 != '\0')) { 
    DAT_c0a9 = '\0';
    DAT_c0aa = 0x20;
    FUN_07cc(1); //    ;)  interesting function as well
  }
  if (DAT_c0aa < 8) { 
    DAT_c0a9 = '\0';
    DAT_c0aa = 0xa0;
    FUN_07cc(0xff);
  }
  if (0xa0 < DAT_c0ac || (byte)(0xa0 - DAT_c0ac) < (DAT_c0ab != '\0')) { // YOU FEEELLLLLLLLLLLLLLL or did YOU RISEEEE UPPP???
    FUN_0150(); // <---- RECURSION!!!!!
  }
```
We have come to a conclusion that the third if statement is responsible for jumping out of the map. What about the other ones? Let's find out by setting breakpoints at them and noting the actions that lead to those statements:

![image](https://user-images.githubusercontent.com/25302752/158213043-6e963065-2dbe-4591-a3e3-d22cf178a181.png)

![right_dir_true](https://user-images.githubusercontent.com/25302752/158218309-d494a0fb-a733-4816-9265-564d05c80832.gif)


Oh, so the first if is responsible for the display of the map block that lies after the right screen border. By repeating these actions with the second if we see that it is responsible for the content behind the left screen border.

But what if the content, that is displayed on the screen after crossing the border depends on the argument, passed to the FUN_077c()? Let's try passing 1 in the second statement.

![win_true](https://user-images.githubusercontent.com/25302752/158218742-57c4accb-c947-4daf-977e-2ad22dda65fa.gif)


WE WON!

All this time the flag was displayed on the level that lies behind the final wall, and we have just bypassed it by displaying the next frame when going left.

Thanks to @ggu for this amazing challenge and everyone who read this wu!

  
  
  
  

  
  
  
