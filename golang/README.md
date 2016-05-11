# 参照 http://www.tuicool.com/articles/r26JRvJ
## 补充

1. 关于google的包无法下载的问题

* github 地址 稍微修改一下路径，这样就可以编译出来这些二进制文件了

* https://github.com/golang/tools.git

> 二进制路径需要加入系统PATH中

2. YouComplete 和 UltiSnips 问题

* 这个教程解决方案并不好，使用supertab 方案明显好一些
都是两个都是用tab补全

* vimrc

```
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
```

3. Tagbar 插件以来gotag，cmake

* go get -u github.com/jstemmer/gotags

* brew install cmake
