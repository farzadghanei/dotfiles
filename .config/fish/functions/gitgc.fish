# Defined in - @ line 1
function gitgc --wraps='git gc --aggressive --prune' --description 'alias gitgc git gc --aggressive --prune'
  git gc --aggressive --prune $argv;
end
