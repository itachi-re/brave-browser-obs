Name:           brave-browser
Version:        1.84.132
Release:        1
Summary:        Brave Web Browser (mirrored binary)
License:        MPL-2.0
URL:            https://brave.com/

#
# === THIS IS THE FIX ===
# The real filename uses "linux-amd64", not "x86_64"
#
Source0:        https://github.com/brave/brave-browser/releases/download/v%{version}/brave-browser-%{version}-x86_64.rpm

ExclusiveArch:  x86_64
AutoReqProv:    no
Conflicts:      brave-browser-beta brave-browser-nightly

Requires:       crontabs
Requires:       /bin/bash
Requires:       fdupes
PreReq:         permissions

%description
Brave is a privacy-focused web browser based on Chromium.
This package is a direct mirror of the official Brave binary release for Fedora/openSUSE.

%prep
#
# === THIS IS THE FIX ===
# Unpack the correct .rpm filename from Source0
#
rpm2cpio %{_sourcedir}/brave-browser-%{version}-linux-amd64.rpm | cpio -idmv

%build
# Nothing to build

%install
#
# === THIS IS THE FIX ===
# Copy the unpacked files from %prep into the buildroot
#
cd %{buildroot}
cp -a %{_builddir}/usr %{buildroot}/
cp -a %{_builddir}/opt %{buildroot}/

# Fix desktop files using sed
sed -i 's/^Type=.*/Type=Application/' %{buildroot}/usr/share/applications/brave-browser.desktop
sed -i 's/^Type=.*/Type=Application/' %{buildroot}/usr/share/applications/com.brave.Browser.desktop

# Ensure Type field exists if it's missing
if ! grep -q '^Type=' %{buildroot}/usr/share/applications/brave-browser.desktop; then
    echo "Type=Application" >> %{buildroot}/usr/share/applications/brave-browser.desktop
fi
if ! grep -q '^Type=' %{buildroot}/usr/share/applications/com.brave.Browser.desktop; then
    echo "Type=Application" >> %{buildroot}/usr/share/applications/com.brave.Browser.desktop
fi

# Remove problematic cron job
rm -f %{buildroot}/etc/cron.daily/brave-browser

%post
%set_permissions /opt/brave.com/brave/chrome-sandbox

%posttrans
# Remove duplicate man pages if fdupes is available
if [ -x /usr/bin/fdupes ]; then
    /usr/bin/fdupes -dN "%{_prefix}/share/man/man1/" 2>/dev/null || true
fi

%verifyscript
%verify_permissions -e /opt/brave.com/brave/chrome-sandbox

%files
/opt/brave.com
/usr/bin/brave-browser-stable
/usr/share/appdata/brave-browser.appdata.xml
/usr/share/applications/brave-browser.desktop
/usr/share/applications/com.brave.Browser.desktop
/usr/share/gnome-control-center/default-apps/brave-browser.xml
/usr/share/man/man1/brave-browser-stable.1.gz
/usr/share/man/man1/brave-browser.1.gz

# Own these directories
%dir /usr/share/appdata
%dir /usr/share/applications
%dir /usr/share/gnome-control-center
%dir /usr/share/gnome-control-center/default-apps

%changelog
