# Install step do have the server

## Linux

### Install Ruby dependencies
```bash
sudo apt-get install ruby-full build-essential zlib1g-dev
```
### Add gem installation directory to PATH (add to ~/.bashrc for permanent)
```bash
echo '# Install Ruby Gems to ~/gems' >> ~/.bashrc
echo 'export GEM_HOME="$HOME/gems"' >> ~/.bashrc
echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc`
```
### Install Jekyll and Bundler
```bash
gem install jekyll bundler
cd /home/alexis/Documents/EPFL/ADA/ada-template-website
bundle install
bundle exec jekyll serve
```

## Windows

### Install Ruby
Download and install Ruby from [RubyInstaller](https://rubyinstaller.org/).

### Install Jekyll and Bundler
Open a **command prompt with ruby** (search with windows button and type ruby) and run:
```
gem install jekyll bundler
bundle install
```

### Create a new Jekyll site
Navigate to the directory where you want to create your site and run:
```
cd /home/alexis/Documents/EPFL/ADA/ada-template-website
bundle exec jekyll serve
```