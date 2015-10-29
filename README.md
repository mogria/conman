# conman, manage configurations with confidence

Tired of having to reconfigure your vim the hundered and second time, because, again you're not at your machine at home?  
Tired of endlessly copying your config files from one machine to an other?  
Or are you just tired of coding all night?

Well the solution is `conman`! (and maybe some sleep, as a second option, of course)  

*Note:* this project is still in early development. Not all commands might work like you would expect, or not work at all.

## How it (should) work:

These are the basic concepts:

 * Your configuration files are managed in a git repository (`.conman` directory).
 * `conman` automatically creates symbolic links to the config files in the repository
 * The `master` branch contains all shared configuration files.
 * The `machine-*` branches contain machine specific configuration files.
 * Each set of configuration files for the same program are organized into modules. (`modules/` directory)
 * On each `machine-*` branch there is a `machine.config` file which specifies which modules are being used.

And the best thing is, the `conman` command manages the git repository for you!

# Install

In the future you should be able to get `conman` via `pip`.

But for now you can also use the install script from github:

    % curl -s https://raw.githubusercontent.com/mogria/conman/master/install-from-web.sh | sh

The script will use `sudo` to execute `python3 setup.py install`.

You can also just clone the repository and add the `conman` executable to your path, if you wish to do so.

# How to use

## Adding a new machine

Run the following command:

    % conman init *git-repo* *machine-name*

The specified `git-repo` should only be used by conman, and you shouldn't just use github or something. Your configs to your e-mail client etc. might contain passwords, and you certainly don't want to publish them on github. Better use a private repo.

If you leave out the `machine-name` the hostname of the machine is used.

## Managing modules

With the following command you can create a new module:

    % conman new *module-name*

To add config files to the module do the following:

    % conman add *module-name* *files...*

It doesn't necessarily need to be a new file, you can update the files with the same command.

But that isn't the whole deal, you need to specify which files will be linked to what location

    % conman link *module-name* *filename* *link-location*

## Managing modules per machine

Now in order to activate a module for the current machine do the following:

    % conman use *module-name*

You can also say that an other machine should use a certain module.

    % conman --machine=*machine-name* use *module-name*

## Replicating configuration to an other machine

To make your configurations and modules accessible to other machines execute:

    % conman push

If you're on an other machine and you want to update the configuration files, just type:

    % conman pull

# Contributing

If you want look at the [the GitHub Repository](https://github.com/mogria/conman) of the project. If you find bugs you can always file an Issue. Pull requests are welcome too!
