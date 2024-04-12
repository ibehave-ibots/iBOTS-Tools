
# Windows Software Resources

This is a collection of installers for various useful programs we use in our work.  

To work automatically, these are all for Windows computers, and assume you're using Windows 11.  That said, most of this software is cross-platform, so if you're on a Mac or Linux computer, it may still be useful and interesting to look into our software packs for ideas on useful software to install (though you'll have to google for the install links yourself.)

## Software Packs

Groups of software around various themes can be found in the `installer_packs` folder.  Just double-click on any packs you'd like to install!  (Note: to see what software is in the packs, you can open the file up in a text editor).  

## Individual Programs

If you want to pick and choose specific software to install, the big list is in  `installer_scripts`, Just double-click on the `.bat` file for any software you want installed.  If we've found an automated installer, then the installer program will run for the latest version of the software.  If we haven't found a nice way to install the latest version of the software, then it will launch a web browser window where the download link can be found.


## Upgrading Your Software

If you want to upgrade all the software already installed by `winget`, you can run:

```
winget upgrade --all
```

If you want to upgrade all the software already installed by `chocolatey`, you can run:

```
choco upgrade all
```

## Contributions Welcome

Have some more suggestions for useful software?  Add it to the lists! Here are the guidelines for keeping consistency across installers:

  1. Scripts should not assume a working directory.  These scripts are meant to be quite user-friendly, so paths in the scripts should be relative to the script's location.
    - Useful Snppet: `%-dp0` (see examples below)
  2. Scripts should be `.bat` files. This is because, despite them being old, they work quite well in Windows environments, and can be run from the file explorer by double-clicking them.
  3. Installer Scripts should be **granular** 
    - Split up programs into multiple installers whenever it's reasonable.
    - Use `CALL` lines to ensure things happen in order.
  4. Installer Scripts should be **independent**
    - scripts should work, and be largely able to be installed in any order.
    - Exception: Plugins.  For plugins, allow them to fail if the software isn't install.
    - Exception: Package Managers. For package managers like `chocolatey` that don't come with windows, the script should handle the installing of the package manager as well.
      - Useful Line: `CALL "%~dp0chocolatey.bat"` will run the chocolatey installer script.
  5. **Installer Packs should depend on the installer scripts**.  
    - Any special installer steps should be put in the installer script file; the packs just call the scripts.
      - Useful Line: `CALL "%~dp0..\installer_scripts\installer_script.bat"`
  6. **Don't be stingy**.  
    - It's okay if there are a few redundant programs included in a pack.  It's hard to be really specific about certain software combinations for people.  By keeping these scripts short, we're trying to make it easy for the optimization-inclined to pick and choose their own software (either by just googling link themselves, or by running installer scripts themselves, or by writing their own packs using our template).  When making packs and trying to decide what to reccomend, this project will push toward over-recommending extra software rather than under-recomending not enough software.  
      - Useful Line: `CALL "%~dp0..\installer_scripts\installer_script.bat"`
  7. **Take Notes**.
    - Feel free to add comments and notes in the installer scripts and packs, to explain the what and why of various software.  Often, that's the most helpful thing you can do for someone.
      - Useful Snippet: `@REM` at the beginning of a line makes it a comment.
  7. **Don't know how to automate the installer?  Don't worry!**.
    - If you at least know where the website with the download link can be found, you can also have the script just use that.  Note that we use Microsoft Edge here, because it's already installed on Windows machines.
      - Useful Snippet: `start microsoft-edge:https://website.com`