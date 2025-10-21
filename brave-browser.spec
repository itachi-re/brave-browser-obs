Name:           brave-browser
Version:        1.83.118
Release:        1
Summary:        Brave Web Browser (mirrored binary)
License:        MPL-2.0
URL:            https://brave.com/
Source0:        brave-browser-%{version}-1.x86_64.rpm.bz2

ExclusiveArch:  x86_64
AutoReqProv:    no
Conflicts:      brave-browser-beta brave-browser-nightly

# Required dependencies
Requires:       crontabs
Requires:       /bin/bash
Requires:       fdupes
PreReq:         permissions

%description
Brave is a privacy-focused web browser based on Chromium.
This package is a direct mirror of the official Brave binary release for Fedora/openSUSE.

%prep
# Empty - we are repackaging a binary RPM, no source to unpack.

%build
# Nothing to build

%install
# Unpack the .rpm file directly into the buildroot
cd %{buildroot}
bzcat %{_sourcedir}/brave-browser-%{version}-1.x86_64.rpm.bz2 | rpm2cpio | cpio -idmv

# Fix desktop files using sed (more reliable than desktop-file-edit)
sed -i 's/^Type=.*/Type=Application/' %{buildroot}/usr/share/applications/brave-browser.desktop
sed -i 's/^Type=.*/Type=Application/' %{buildroot}/usr/share/applications/com.brave.Browser.desktop

# Ensure Type field exists if it's missing
if ! grep -q '^Type=' %{buildroot}/usr/share/applications/brave-browser.desktop; then
    echo "Type=Application" >> %{buildroot}/usr/share/applications/brave-browser.desktop
fi
if ! grep -q '^Type=' %{buildroot}/usr/share/applications/com.brave.Browser.desktop; then
    echo "Type=Application" >> %{buildroot}/usr/share/applications/com.brave.Browser.desktop
fi

# Remove problematic cron job (Brave updates itself internally)
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
* Mon Oct 20 2025 itachi_re <xanbenson99@gmail.com> 1.83.118-1
- Mirrored Brave browser binary from GitHub
- Fixed RPMLint errors: removed cron job, fixed desktop files with sed
- Added fdupes to handle duplicate man pages in posttrans