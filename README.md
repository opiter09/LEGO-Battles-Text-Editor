# LEGO-Battles-Text-Editor
This is just some code to let you edit the text of the NDS game LEGO Battles (and its beta version). All you have to do is drag your ROM
onto lang.exe, and then (after some time), edit the text files inside of the "_langFiles" folders. When you're done, just drag the ROM onto
lang.exe again to yield the new ROM "out.nds", along with the XDelta patch file "out.xdelta" ready to distribute.

NOTE: Unlike previous versions of this tool, the current one makes use of NDSTool. This does not play nice with CrystalTile2 for some
reason, so to use individually edited non-text files, please insert them into the folder NDS_UNPACK here after generating the text files.

To download this, you'll need to find and press the green "Code" button, then press "Download ZIP." It's weird, I know.

# Source Codes
- NDSTool: https://github.com/devkitPro/ndstool (this is a later version; the one used here came without a license as part of DSLazy)
- xdelta: https://github.com/jmacd/xdelta-gpl
