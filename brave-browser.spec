#
# spec file for package brave-browser
#
# Copyright (c) 2026 SUSE LLC and contributors
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

%global debug_package %{nil}
%global __spec_install_post %{nil}

Name:           brave-browser
Version:        1.92.144
Release:        1
Summary:        Brave Web Browser (mirrored binary)
License:        MPL-2.0
URL:            https://brave.com/
Vendor:         Brave Software, Inc.
Group:          Productivity/Networking/Web/Browsers

Source0:        https://github.com/brave/brave-browser/releases/download/v%{version}/brave-browser-%{version}-1.x86_64.rpm
Source1:        brave-wayland.sh

ExclusiveArch:  x86_64
AutoReqProv:    no
Conflicts:      brave-browser-beta brave-browser-nightly

Requires:       /bin/bash

BuildRequires:  cpio
BuildRequires:  fdupes

%description
Brave is a privacy-focused web browser based on Chromium.

This package is a direct binary mirror of the official Brave stable release
for Fedora/openSUSE (x86_64).

%prep
cd %{_builddir}
rpm2cpio %{SOURCE0} | cpio -idmv --no-absolute-filenames

%build

%install
cp -a %{_builddir}/usr  %{buildroot}/
cp -a %{_builddir}/opt  %{buildroot}/

rm -f %{buildroot}%{_datadir}/applications/com.brave.Browser.desktop

sed -i 's/^Type=.*/Type=Application/' \
    %{buildroot}%{_datadir}/applications/brave-browser.desktop

if ! grep -q '^Type=' \
       %{buildroot}%{_datadir}/applications/brave-browser.desktop; then
    echo "Type=Application" >> \
        %{buildroot}%{_datadir}/applications/brave-browser.desktop
fi

rm -f %{buildroot}/etc/cron.daily/brave-browser
rmdir --ignore-fail-on-non-empty %{buildroot}/etc/cron.daily 2>/dev/null || true
rmdir --ignore-fail-on-non-empty %{buildroot}/etc             2>/dev/null || true

install -Dm 0644 %{SOURCE1} \
    %{buildroot}/etc/profile.d/brave-wayland.sh

fdupes -dN %{buildroot}%{_mandir}/man1/ 2>/dev/null || true

%post
chmod 4755 /opt/brave.com/brave/chrome-sandbox || true

%posttrans
:

%verifyscript
[ -u /opt/brave.com/brave/chrome-sandbox ] || exit 1

%files
%defattr(-,root,root,-)

/opt/brave.com
%{_bindir}/brave-browser-stable

%{_datadir}/appdata/brave-browser.appdata.xml
%{_datadir}/applications/brave-browser.desktop
%{_datadir}/gnome-control-center/default-apps/brave-browser.xml
%dir %{_datadir}/gnome-control-center
%dir %{_datadir}/gnome-control-center/default-apps

%{_mandir}/man1/brave-browser-stable.1.gz
%{_mandir}/man1/brave-browser.1.gz

%config(noreplace) /etc/profile.d/brave-wayland.sh

%changelog
* Wed Apr 29 2026 itachi-re <xanbenson99@gmail.com> - 1.89.143-1
- Initial OBS package: binary mirror of official Brave x86_64 RPM
- Removed upstream cron job (not appropriate for openSUSE)
- Removed duplicate com.brave.Browser.desktop
- Added Wayland/Ozone profile.d hint for KDE Plasma (Wayland)
- Fixed chrome-sandbox permissions via openSUSE permissions framework
