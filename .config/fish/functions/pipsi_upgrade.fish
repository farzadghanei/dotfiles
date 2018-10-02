function --description "Upgrade all packages managed by pipsi" pipsi_upgrade
    set -l packages (pipsi list  | grep -oP 'Package ".+"' | awk '{print $NF}' | sed 's/"//g')
    for package in $packages
        pipsi upgrade $package
    end
end
