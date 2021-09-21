# Defined in - @ line 1
function gita --wraps='git add -u' --description 'alias gita git add -u'
  git add -u $argv;
end
