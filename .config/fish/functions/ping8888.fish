# Defined via `source`
function ping8888 --wraps='ping 8.8.8.8' --description 'alias ping8888 ping 8.8.8.8'
  ping 8.8.8.8 $argv; 
end
