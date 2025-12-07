# Install step do have the server

## Install Ruby dependencies
sudo apt-get install ruby-full build-essential zlib1g-dev
## Add gem installation directory to PATH (add to ~/.bashrc for permanent)
echo '# Install Ruby Gems to ~/gems' >> ~/.bashrc
echo 'export GEM_HOME="$HOME/gems"' >> ~/.bashrc
echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
## Install Jekyll and Bundler
gem install jekyll bundler
cd /home/alexis/Documents/EPFL/ADA/ada-template-website
bundle install
bundle exec jekyll serve