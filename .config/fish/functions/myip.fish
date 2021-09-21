# Defined via `source`
function myip --wraps='curl -4 icanhazip.com' --description 'alias myip curl -4 icanhazip.com'
  curl -4 icanhazip.com $argv; 
end
