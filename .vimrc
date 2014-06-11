""" Vundle Entries
set nocompatible               " be iMproved
filetype off                   " required!

set runtimepath+=~/.vim/bundle/vundle/
call vundle#rc()

" Bundles here:
"
" shortnames come from http://github.com
" long names could include a git repo URL
"
" Run :BundleInstall! to install/update bundles
"
" let Vundle manage Vundle
" required! 
Bundle 'gmarik/vundle'

Bundle 'tpope/vim-fugitive'
Bundle 'jeetsukumaran/vim-buffergator'
Bundle 'Lokaltog/vim-easymotion'
Bundle 'mileszs/ack.vim'
Bundle 'ddollar/nerdcommenter'
Bundle 'ervandew/supertab'

Bundle 'majutsushi/tagbar'
  nmap <F4> :TagbarToggle<CR>

Bundle 'airblade/vim-gitgutter'
  let g:gitgutter_sign_column_always = 0

Bundle 'vim-scripts/The-NERD-tree'
  map <F3> :NERDTreeToggle<CR>
  let NERDTreeWinPos = 'left'

" YouCompeleteMe requires vim 7.3+
" Bundle 'Valloric/YouCompleteMe'

Bundle 'kien/ctrlp.vim'
  let g:ctrlp_working_path_mode = 0 " dont manage working directory.
  let g:ctrlp_custom_ignore = {
  \ 'dir':  '\v\c\.(git|svn)$',
  \ 'file': '\v\c\.(swf|bak|png|gif|mov|ico|jpg|pdf)$',
  \ }

Bundle 'Lokaltog/vim-powerline'
  let g:Powerline_symbols = 'fancy'
  highlight clear SignColumn

" lang specific modules
Bundle 'c9s/perlomni.vim'
Bundle 'cakebaker/scss-syntax.vim'

filetype plugin indent on     " required!

""" vimrc resumes
set shell=bash
set autoindent
set backspace=indent,eol,start
set nowrap

# Line Numbers
set nu
set rnu
highlight LineNr term=bold cterm=NONE ctermfg=DarkGrey ctermbg=NONE gui=NONE guifg=DarkGrey guibg=NONE

set ruler
set scrolloff=5
set cmdheight=2
set cursorcolumn
set cursorline
set errorformat=\"../../%f\"\\,%*[^0-9]%l:\ %m
set hidden
set hlsearch
set ignorecase
set incsearch
set laststatus=2
set list
set listchars=tab:▸\ ,trail:-,eol:¬
set expandtab
set shiftwidth=4
set smarttab
set cindent
"set smartindent
set showcmd
set showmatch
set t_Co=256
set tags=tags;/
set virtualedit=block
set mouse=n
set ttymouse=xterm2
set backupdir=~/tmp
set wildmenu
set wildignore=*.exe,*.dll,*.o,*.so,*.pyc,*.back,*.jpg,*.jpeg,*.png,*.gif,*.pdf
set wildmode=list:full

syntax on
colorscheme colorfulnight


" :help last-position-jump
autocmd BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g`\"" | endif

nnoremap <C-L> :noh<CR><C-L>
inoremap jj <Esc>
nnoremap <Leader>r :source ~/.vimrc<CR>
nnoremap <Leader><Leader>r :e ~/.vimrc<CR>
map <Leader>gs :Gstatus<CR>
map <Leader>gc :Gcommit<CR>
map <Leader>gm :Gcommit --amend<CR>
map <Leader>gll :Git log<CR>
map <Leader>glp :Git log -p<CR>
map <Leader>gb :Gblame<CR>
map <Leader>gdd :Git diff<CR>
map <Leader>gdm :Git diff %<CR>
map <Leader>gdf :Gdiff<CR>
map <Leader>gg :Git 

nmap <F1> <Esc>
imap <F1> <Esc>

nnoremap <C-S-K> :m .-2<CR>==
nnoremap <C-S-J> :m .+1<CR>==
inoremap <C-S-J> <Esc>:m .+1<CR>==gi
inoremap <C-S-K> <Esc>:m .-2<CR>==gi
vnoremap <C-S-K> :m '<-2<CR>gv=gv
vnoremap <C-S-J> :m '>+1<CR>gv=gv

# Map <Ctrl+N> to toggle relative line numbers
nmap <C-N> :set invrnu<CR>

# switch the line-number style, in normal mode, and insert mode
au FocusLost * :set number
au FocusGained * :set relativenumber
au InsertEnter * :set number
au InsertLeave * :set relativenumber

# Use F2 to toggle set paste
nnoremap <F2> :set invpaste paste?<CR>
set pastetoggle=<F2>
