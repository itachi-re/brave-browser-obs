# /etc/profile.d/brave-wayland.sh
#
# Installed by the brave-browser OBS package.
# Sets the Chromium/Ozone platform hint to "auto" so that Brave Browser
# automatically selects native Wayland when running under a Wayland compositor
# (e.g. KDE Plasma on Wayland) and falls back to XWayland otherwise.
#
# To override system-wide, set ELECTRON_OZONE_PLATFORM_HINT in your shell's
# own profile or in ~/.config/BraveSoftware/Brave-Browser/brave_flags.conf.
#
# Reference: https://wiki.archlinux.org/title/Chromium#Native_Wayland_support

export ELECTRON_OZONE_PLATFORM_HINT="${ELECTRON_OZONE_PLATFORM_HINT:-auto}"

