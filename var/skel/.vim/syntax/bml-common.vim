if exists("b:current_syntax")
	unlet b:current_syntax
endif
syn include @HTML syntax/html.vim
unlet b:current_syntax
syn include @Perl syntax/perl.vim
unlet b:current_syntax

syn cluster htmlPreproc add=@bmlBlock,bmlData

syn cluster bmlHTMLData contains=@HTML,bmlData
syn cluster bmlDefinition contains=bmlSingleDefinition,bmlMultiDefinition
syn cluster bmlBlock contains=bmlClosedBlock,bmlOpenBlock,@bmlSpecialBlocks
syn cluster bmlSpecialBlocks contains=bmlCodeBlock,bmlLanguageBlock,bmlCommentBlock,bmlInfoBlock,bmlEHBlock,bmlEBBlock,bmlEABlock

syn region  bmlData start="%%" end="%%" contained

hi def link bmlDefinition Identifier
hi def link bmlBlock PreProc
hi def link bmlData Special

syn region  bmlSingleDefinition matchgroup=bmlDefinition start="^\([a-zA-Z0-9_/]\+\)=>" end="$" contains=@bmlHTMLData,@bmlBlock oneline contained
syn region  bmlMultiDefinition matchgroup=bmlDefinition start="^\z([a-zA-Z0-9_/]\+\)<=" end="<=\z1$" contains=@bmlHTMLData,@bmlBlock contained
syn region  bmlLocalBlocksDefinition matchgroup=bmlDefinition start="^localblocks<=$" end="^<=localblocks$" contains=@bmlDefinition contained

syn match   bmlClosedBlock "<?[a-zA-Z_/]\+?>" contained
hi def link bmlClosedBlock bmlBlock
syn region  bmlOpenBlock matchgroup=bmlBlock start="<?\z([a-zA-Z0-9_/]\+\)\>\(?>\)\@!" end="\<\z1?>" contains=bmlPipeChar,@bmlHTMLData,@bmlBlock,@bmlDefinition contained
syn match   bmlPipeChar "|" contained
hi def link bmlPipeChar Special

syn region  bmlCodeBlock matchgroup=bmlBlock start="<?_code\>\(?>\)\@!" end="\<_code?>" contains=@Perl contained
syn region  bmlLanguageBlock matchgroup=bmlBlock start="<?_ml\>\(?>\)\@!" end="\<_ml?>" contained
syn region  bmlCommentBlock matchgroup=bmlBlock start="<?_c\>\(?>\)\@!" end="\<_c?>" contained
syn region  bmlInfoBlock matchgroup=bmlBlock start="<?_info\>\(?>\)\@!" end="\<_info?>" contains=bmlLocalBlocksDefinition,@bmlDefinition contained
syn region  bmlEHBlock matchgroup=bmlBlock start="<?_eh\>\(?>\)\@!" end="\<_eh?>" contains=bmlData,@bmlBlock contained
"bmlEBBlock doesn't work properly right now
"syn region  bmlEBBlock matchgroup=bmlBlock start="<?_eb\>\(?>\)\@!" end="\<_eb?>" contains=@bmlHTMLData contained
syn region  bmlEABlock matchgroup=bmlBlock start="<?_ea\>\(?>\)\@!" end="\<_ea?>" contains=bmlData contained

hi def link bmlLanguageBlock Constant
hi def link bmlCommentBlock Comment
