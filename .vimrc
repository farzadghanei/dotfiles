""" Vundle Entries
set nocompatible               " be iMproved
filetype off                   " required!

"Use plug.vim to install plugins

call plug#begin('~/.vim/plugged')

" themese/colors
Plug 'jacoborus/tender.vim'

" this assumes fzf is installed separately on ~/.apps/fzf
" see https://github.com/junegunn/fzf
" Plug '~/.apps/fzf' | Plug 'junegunn/fzf.vim'
Plug 'junegunn/fzf.vim'
  noremap <C-P> :Files<CR>
  noremap <C-T> :Rg<CR>
  noremap <Leader>t :Buffers<CR>

Plug 'easymotion/vim-easymotion'

Plug 'tpope/vim-surround'
Plug 'tpope/vim-fugitive'
Plug 'tpope/vim-commentary'
" or
"Plug 'scrooloose/nerdcommenter'

" file explorer using netrw
Plug 'tpope/vim-vinegar'

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

" autoclose brackets,parens, ...
" Plug 'jiangmiao/auto-pairs'

"Plug 'ctrlpvim/ctrlp.vim'
"  let g:ctrlp_working_path_mode = 0 " dont manage working directory.
"  let g:ctrlp_custom_ignore = {
"  \ 'dir':  '\v\c\.(git|svn|tox|nox)$',
"  \ 'file': '\v\c\.(swf|bak|png|gif|mov|ico|jpg|pdf)$',
"  \ }

Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
  let g:airline_theme='powerlineish'

Plug 'vim-vdebug/vdebug'
Plug 'github/copilot.vim', { 'branch': 'release' }
   " disable copilot for specific file types
   let g:copilot_filetypes = {
        \ 'xml': v:true,
        \ }
   "let g:copilot_proxy = 'localhost:3128'
  nnoremap <Leader>co :Copilot panel<CR>
  nnoremap <Leader>cos :Copilot status<CR>

" lang specific modules
Plug 'dense-analysis/ale'  " multi lang linter/fixers
  let g:ale_linters_explicit = 0  " enable/disable all linters by default, only enable explicit ones
  let g:ale_pattern_options_enabled = 1  " enable ALE for specific file types options
  let g:ale_pattern_options = {'\.yaml\|yml$': {'ale_enabled': 1}}  " disable ALE for specific file types (yaml, ...)
  let g:ale_linters = {'python': ['ruff', 'mypy'], 'yaml': ['yamllint'], 'go': ['gopls', 'golangci-lint']}
  let g:ale_fixers = {'python': ['black'], 'go': ['gofmt', 'goimports']}
  let g:ale_disable_lsp = 1  " disable language server integration (use jedi-vim)
  let g:ale_fix_on_save = 1
  let g:ale_fix_on_save = 1
  let g:ale_history_enabled = 1
  let g:ale_hover_cursor = 1
  "let b:ale_fix_on_save_ignore = {'filetype': ['fixer']}
  nnoremap <Leader>af :ALEFix<CR>

Plug 'davidhalter/jedi-vim' " python autocomplete, etc. installed with rpm jedi-vim
    let g:jedi#completions_command = "<C-Space>"
    let g:jedi#rename_command = "<Leader>r"
    let g:jedi#popup_on_dot = 1
    let g:jedi#popup_select_first = 1
    let g:jedi#smart_auto_mappings = 1  " automatically add the "import" trigger the autocompletion popup

Plug 'ekalinin/Dockerfile.vim'
Plug 'fatih/vim-go', { 'do': ':GoUpdateBinaries' }
    " explicit defaults
    let g:go_code_completion_enabled = 1
    let g:go_fmt_autosave = 1
    let g:go_imports_autosave = 1
    let g:go_doc_keywordprg_enabled = 1
    let g:go_metalinter_autosave_enabled = ['all']
    let g:go_metalinter_enabled = ['vet', 'revive', 'errcheck']
    " overrdie defaults
    let g:go_test_show_name = 1  " 0: Show the name of each failed test before the errors and logs output by the test
    let g:go_auto_type_info = 1  " 0
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
"nnoremap <Leader>r :source ~/.vimrc<CR>  # collides with jedi#rename_command
nnoremap <Leader><Leader>r :e ~/.vimrc<CR>
map <Leader>gs :Git status<CR>
map <Leader>gc :Git commit<CR>
map <Leader>gm :Git commit --amend<CR>
map <Leader>gll :Git log<CR>
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
