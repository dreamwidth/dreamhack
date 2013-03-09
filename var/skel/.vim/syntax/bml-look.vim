" Vim syntax file

" Remove any old syntax stuff that was loaded (5.x) or quit when a syntax file
" was already loaded (6.x).
if version < 600
  syntax clear
elseif exists("b:current_syntax")
  finish
endif

" we need to define these two again without 'contained'. I wish there was a
" way to do this for existing definitions.
syn region  bmlSingleDefinition matchgroup=bmlDefinition start="^\([a-zA-Z0-9_/]\+\)=>" end="$" contains=@bmlHTMLData,@bmlBlock oneline
syn region  bmlMultiDefinition matchgroup=bmlDefinition start="^\z([a-zA-Z0-9_/]\+\)<=" end="<=\z1$" contains=@bmlHTMLData,@bmlBlock

" This type of comment is only valid in the root of a .look file.
syn match   bmlComment "^#.*"
hi def link bmlComment Comment

runtime! syntax/bml-common.vim
