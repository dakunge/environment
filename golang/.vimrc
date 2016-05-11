syntax on
set nu
colorscheme molokai

set nocompatible              " be iMproved, required
filetype off                  " required

" about plugin
" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()


" let Vundle manage Vundle, required
Plugin 'gmarik/Vundle.vim'
Plugin 'fatih/vim-go'
Plugin 'Valloric/YouCompleteMe'
Plugin 'SirVer/ultisnips'
Plugin 'ervandew/supertab'
Plugin 'Tagbar'

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required


set nowritebackup
set autochdir  " 自动切换当前目录为当前文件所在的目录
set ignorecase  " 搜索时忽略大小写，但在有一个或以上大写字母时仍大小写敏感
set nowrapscan " 搜索到文件两端时不重新搜索
set incsearch  " 实时搜索
set hlsearch  " 搜索时高亮显示被找到的文本
set number   " 显示行号
set hidden    " 允许在有未保存的修改时切换缓冲区
set wildmenu " 开启命令行补全
set smartindent " 智能自动缩进
set scrolloff=3  " 上下可视行数
set nocursorline  " 不突出显示当前行
set showmatch  "显示括号配对情况
set shortmess=atl  "启动时不显示 捐赠提示
set ruler
set incsearch  "实时搜索
set tabstop=4      "tab键为4个空格
set shiftwidth=4   "换行时行间交错使用4个空格
set nobackup       "     不要备份文件
set expandtab "用space替代tab的输入 set noexpandtab 不用space替代tab的输入
" No annoying sound on errors  
" 去掉输入错误的提示声音  
set noerrorbells  
set novisualbell
set vb t_vb=
" vi中复制的内容同时复制到剪切板
set clipboard+=unnamed

""为方便复制，用<F2>开启/关闭行号显示:  
nnoremap <F2> :set nonumber!<CR>:set foldcolumn=0<CR> 
autocmd BufReadPost *
\ if line("'\"")>0&&line("'\"")<=line("$") |
\   exe "normal g'\"" |
\ endif

" go get -u github.com/jstemmer/gotags
" brew install cmake
" tagbar + gotag"
let g:tagbar_type_go = {
    \ 'ctagstype' : 'go',
    \ 'kinds'     : [
        \ 'p:package',
        \ 'i:imports:1',
        \ 'c:constants',
        \ 'v:variables',
        \ 't:types',
        \ 'n:interfaces',
        \ 'w:fields',
        \ 'e:embedded',
        \ 'm:methods',
        \ 'r:constructor',
        \ 'f:functions'
    \ ],
    \ 'sro' : '.',
    \ 'kind2scope' : {
        \ 't' : 'ctype',
        \ 'n' : 'ntype'
    \ },
    \ 'scope2kind' : {
        \ 'ctype' : 't',
        \ 'ntype' : 'n'
    \ },
    \ 'ctagsbin'  : 'gotags',
    \ 'ctagsargs' : '-sort -silent'
    \ }

" make YCM compatible with UltiSnips (using supertab)
let g:ycm_key_list_select_completion = ['<C-n>', '<Down>']
let g:ycm_key_list_previous_completion = ['<C-p>', '<Up>']
let g:SuperTabDefaultCompletionType = '<C-n>'
"
" " better key bindings for UltiSnipsExpandTrigger
let g:UltiSnipsExpandTrigger = "<tab>"
let g:UltiSnipsJumpForwardTrigger = "<tab>"
let g:UltiSnipsJumpBackwardTrigger = "<s-tab>"

"about go
"set mapleader
let mapleader = ","

" vim-go custom mappings
au FileType go nmap <Leader>s <Plug>(go-implements)
au FileType go nmap <Leader>i <Plug>(go-info)
au FileType go nmap <Leader>gd <Plug>(go-doc)
au FileType go nmap <Leader>gv <Plug>(go-doc-vertical)
au FileType go nmap <leader>r <Plug>(go-run)
au FileType go nmap <leader>b <Plug>(go-build)
au FileType go nmap <leader>t <Plug>(go-test)
au FileType go nmap <leader>c <Plug>(go-coverage)
au FileType go nmap <Leader>ds <Plug>(go-def-split)
au FileType go nmap <Leader>dv <Plug>(go-def-vertical)
au FileType go nmap <Leader>dt <Plug>(go-def-tab)
au FileType go nmap <Leader>e <Plug>(go-rename)

let g:go_fmt_command = "goimports"

nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l
let g:tagbar_left = 1
let g:tagbar_width = 25
let g:tagbar_autofocus = 1
let g:tagbar_sort = 0
