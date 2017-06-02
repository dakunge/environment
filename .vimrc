syntax on
set nu
colorscheme molokai

set backspace=indent,eol,start " 解决不能使用delete 退格问题
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
Plugin 'godlygeek/tabular' " markdown 工具，有顺序要求
Plugin 'plasticboy/vim-markdown'
Plugin 'suan/vim-instant-markdown'
Plugin 'python.vim'
Plugin 'ctrlpvim/ctrlp.vim'
" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required


set nowritebackup
set autochdir  " 自动切换当前目录为当前文件所在的目录
"set ignorecase  " 搜索时忽略大小写，但在有一个或以上大写字母时仍大小写敏感
set nowrapscan " 搜索到文件两端时不重新搜索
set incsearch  " 实时搜索
set hlsearch  " 搜索时高亮显示被找到的文本
set number   " 显示行号
set hidden    " 允许在有未保存的修改时切换缓冲区
set wildmenu " 开启命令行补全
set smartindent " 智能自动缩进
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
" 解决复制的缩进问题，每次复制前F3，复制后F3
set pastetoggle=<F3>
" vim_markdown
let g:vim_markdown_folding_disabled=1

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

" vim-go
let g:go_fmt_command = "goimports"
let g:go_autodetect_gopath = 1
let g:go_list_type = "quickfix"

let g:go_highlight_types = 1
let g:go_highlight_fields = 1
let g:go_highlight_functions = 1
let g:go_highlight_methods = 1
let g:go_highlight_extra_types = 1
let g:go_highlight_generate_tags = 1

"let g:go_def_reuse_buffer = 1
let g:go_def_mode = 'godef'
"let g:go_def_mode = 'guru'


" Open :GoDeclsDir with ctrl-g
"nmap <C-g> :GoDeclsDir<cr>
"imap <C-g> <esc>:<C-u>GoDeclsDir<cr>

nmap <C-i> :GoSameIdsToggle<cr>

" vim-go custom mappings
au FileType go nmap <Leader>is <Plug>(go-implements)
au FileType go nmap <Leader>cs <Plug>(go-callstack)
au FileType go nmap <leader>c <Plug>(go-callers)
au FileType go nmap <Leader>rn <Plug>(go-rename)
au FileType go nmap <Leader>i <Plug>(go-describe)
au FileType go nmap <Leader>p <Plug>(go-channelpeers)
au FileType go nmap <Leader>e <Plug>(go-whicherrs)
au FileType go vmap <Leader>f <Plug>(go-freevars)
au FileType go nmap <Leader>r <Plug>(go-referrers)

  " :GoAlternate  commands :A, :AV, :AS and :AT
  autocmd Filetype go command! -bang A call go#alternate#Switch(<bang>0, 'edit')
  autocmd Filetype go command! -bang AV call go#alternate#Switch(<bang>0, 'vsplit')
  autocmd Filetype go command! -bang AS call go#alternate#Switch(<bang>0, 'split')
  autocmd Filetype go command! -bang AT call go#alternate#Switch(<bang>0, 'tabe')

"au FileType go nmap <Leader>bar :Tagbar<CR>
nmap <Leader>bar :Tagbar<CR>
map <C-o> <C-t>

nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l
let g:tagbar_left = 1
let g:tagbar_width = 25
let g:tagbar_autofocus = 1
let g:tagbar_sort = 0

" 复制不规则
" :set paste 和 :set nopaste
"
let g:syntastic_go_checkers = ['errcheck']
"let g:go_metalinter_autosave = 1
"let g:go_metalinter_deadline = "5s"
"let g:go_metalinter_autosave_enabled = ['vet', 'err']
let g:go_metalinter_autosave_enabled = ['err']

let g:syntastic_mode_map = { 'mode': 'active', 'passive_filetypes': ['go'] }

"let g:go_guru_scope = ["github.com/hyperledger/fabric/orderer"]
"let g:go_guru_scope = ["increment-only-counter"]
"let g:go_guru_scope = ["github.com/hyperledger/fabric/peer", "seaweedfs/weed", "github.com/hyperledger/fabric-ca/cmd/fabric-ca-server"]
let g:go_guru_scope = ["github.com/hyperledger/fabric/peer"]

"let g:go_guru_scope = ["..."]
