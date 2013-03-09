" Vim syntax file

" Remove any old syntax stuff that was loaded (5.x) or quit when a syntax file
" was already loaded (6.x).
if version < 600
  syntax clear
elseif exists("b:current_syntax")
  finish
endif

runtime! syntax/html.vim

" we need to define the blocks again without 'contained'. I wish there was a
" way to do this for existing definitions.
syn match   bmlClosedBlock "<?[a-zA-Z_/]\+?>"
syn region  bmlOpenBlock matchgroup=bmlBlock start="<?\z([a-zA-Z0-9_/]\+\)\>\(?>\)\@!" end="\<\z1?>" contains=bmlPipeChar,@bmlHTMLData,@bmlBlock,@bmlDefinition

syn region  bmlCodeBlock matchgroup=bmlBlock start="<?_code\>\(?>\)\@!" end="\<_code?>" contains=@Perl
syn region  bmlLanguageBlock matchgroup=bmlBlock start="<?_ml\>\(?>\)\@!" end="\<_ml?>"
syn region  bmlCommentBlock matchgroup=bmlBlock start="<?_c\>\(?>\)\@!" end="\<_c?>"
syn region  bmlInfoBlock matchgroup=bmlBlock start="<?_info\>\(?>\)\@!" end="\<_info?>" contains=bmlLocalBlocksDefinition,@bmlDefinition
syn region  bmlEHBlock matchgroup=bmlBlock start="<?_eh\>\(?>\)\@!" end="\<_eh?>" contains=bmlData,@bmlBlock
"bmlEBBlock doesn't work properly right now
"syn region  bmlEBBlock matchgroup=bmlBlock start="<?_eb\>\(?>\)\@!" end="\<_eb?>" contains=@bmlHTMLData
syn region  bmlEABlock matchgroup=bmlBlock start="<?_ea\>\(?>\)\@!" end="\<_ea?>" contains=bmlData

runtime! syntax/bml-common.vim
