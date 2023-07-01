""" Vundle Entries
set nocompatible               " be iMproved
filetype off                   " required!

"Use plug.vim to install plugins
call plug#begin('~/.vim/plugged')

" this assumes fzf is installed separately on ~/.apps/fzf
" see https://github.com/junegunn/fzf
"Plug '~/.apps/fzf' | Plug 'junegunn/fzf.vim'
Plug 'junegunn/fzf.vim'
  noremap <C-P> :Files<CR>
  noremap <C-T> :Rg<CR>
  noremap <Leader>t :Buffers<CR>

Plug 'tpope/vim-surround'
Plug 'tpope/vim-fugitive'
Plug 'tpope/vim-commentary'
" or
"Plug 'scrooloose/nerdcommenter'
" file explorer using netrw
Plug 'tpope/vim-vinegar'

Plug 'Lokaltog/vim-easymotion'

" autoclose brackets,parens, ...
Plug 'jiangmiao/auto-pairs'

Plug 'majutsushi/tagbar'
  nmap <F4> :TagbarToggle<CR>

Plug 'airblade/vim-gitgutter'
  let g:gitgutter_sign_column_always = 0

Plug 'vim-scripts/The-NERD-tree'
  let NERDTreeWinPos = 'left'
  map <F3> :NERDTreeToggle<CR>
  nnoremap <Leader>ff :NERDTreeFind<CR>
  let NERDTreeQuitOnOpen = 1  " auto close tree upon file open
  let NERDTreeAutoDeleteBuffer = 1  " del buffer when tree del a file
  let NERDTreeMinimalUI = 1
  let NERDTreeDirArrows = 1


"Plug 'ctrlpvim/ctrlp.vim'
"  let g:ctrlp_working_path_mode = 0 " dont manage working directory.
"  let g:ctrlp_custom_ignore = {
"  \ 'dir':  '\v\c\.(git|svn)$',
"  \ 'file': '\v\c\.(swf|bak|png|gif|mov|ico|jpg|pdf)$',
"  \ }

Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
  let g:airline_theme='powerlineish'

Plug 'vim-vdebug/vdebug'

" lang specific modules
Plug 'ekalinin/Dockerfile.vim'
Plug 'fatih/vim-go', { 'do': ':GoUpdateBinaries' }
Plug 'davidhalter/jedi-vim'

"Plug 'python-mode/python-mode'
"Plug 'c9s/perlomni.vim'
"Plug 'puppetlabs/puppet-syntax-vim'

"Plug 'rust-lang/rust.vim'

" required by vim-markdown. Text alignment and filtering
" Plug 'godlygeek/tabular'
" Plug 'plasticboy/vim-markdown'
"    let g:vim_markdown_no_default_key_mappings = 1
"    let g:vim_markdown_folding_disabled = 1

call plug#end()

""" vimrc resumes
set shell=bash
set autoindent
set backspace=indent,eol,start
set nowrap
set number
set ruler
set scrolloff=5
set cmdheight=2
set cursorcolumn
set cursorline
set errorformat=\"../../%f\"\\,%*[^0-9]%l:\ %m
set hidden
set hlsearch
set noignorecase
set incsearch
set laststatus=2
set list
set listchars=tab:>-,trail:-
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
"set mouse=n
"set ttymouse=xterm2
set backupdir=~/tmp
set wildmenu
set wildignore=*.exe,*.dll,*.o,*.so,*.pyc,*.back,*.jpg,*.jpeg,*.png,*.gif,*.pdf
set wildmode=list:full
set colorcolumn=80

syntax on
colorscheme colorfulnight


" :help last-position-jump
autocmd BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g`\"" | endif

nnoremap <C-L> :noh<CR><C-L>
inoremap jj <Esc>
noremap ff :
noremap rr :w!<CR>
noremap vv :wq<CR>
nnoremap <Leader>r :source ~/.vimrc<CR>
nnoremap <Leader><Leader>r :e ~/.vimrc<CR>
map <Leader>gc :Git commit<CR>
map <Leader>gs :Git status<CR>
map <Leader>gm :Git commit --amend<CR>
map <Leader>gl :Git log<CR>
map <Leader>glp :Git log -p<CR>
map <Leader>gb :Git blame<CR>
map <Leader>gdd :Git diff<CR>
map <Leader>gdm :Git diff %<CR>
map <Leader>gg :Git 

nmap <F1> <Esc>
imap <F1> <Esc>

nnoremap <C-S-K> :m .-2<CR>==
nnoremap <C-S-J> :m .+1<CR>==
inoremap <C-S-J> <Esc>:m .+1<CR>==gi
inoremap <C-S-K> <Esc>:m .-2<CR>==gi
vnoremap <C-S-K> :m '<-2<CR>gv=gv
vnoremap <C-S-J> :m '>+1<CR>gv=gv
vnoremap // y/<C-R>"<CR>
