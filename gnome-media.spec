Summary:	GNOME media programs
Name:		gnome-media
Version:	2.91.2
Release:	1
License:	GPLv2+ and GFDL+
Group:		Graphical desktop/GNOME
URL:		http://www.gnome.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: desktop-file-utils
BuildRequires: gnome-doc-utils
BuildRequires: intltool >= 0.35
BuildRequires: pkgconfig(gnome-keybindings) >= 3.2.2
BuildRequires: pkgconfig(gstreamer-0.10)
BuildRequires: pkgconfig(gconf-2.0)
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(libcanberra-gtk3)
BuildRequires: pkgconfig(libgnome-media-profiles-3.0)
BuildRequires: pkgconfig(libpulse)
BuildRequires: pkgconfig(libxml-2.0)

Requires:   gstreamer0.10-plugins-good
Requires:   gstreamer0.10-plugins-base
Suggests:   gstreamer0.10-flac
Suggests:   gstreamer0.10-speex
Requires(post,preun):	GConf2

%description
This package contains a few media utilities for the GNOME desktop,
including a sound recorder and an audio mixer.

%prep
%setup -q 
%apply_patches

%build

%configure2_5x \
	--disable-static

%make

%install
rm -rf %{buildroot} *.lang
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

desktop-file-install --vendor="" \
	--add-category="DesktopSettings" \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/gstreamer-properties.desktop

desktop-file-install --vendor="" \
	--add-category="X-MandrivaLinux-CrossDesktop" \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/gnome-sound-recorder.desktop

%find_lang %{name}-2.0 --with-gnome --all-name

%files -f  %{name}-2.0.lang
%doc AUTHORS NEWS README
%{_sysconfdir}/gconf/schemas/gnome-sound-recorder.schemas
%{_bindir}/*
%{_datadir}/applications/gnome-sound-recorder.desktop
%{_datadir}/applications/gstreamer-properties.desktop
%{_datadir}/gnome-media
%{_datadir}/gnome-sound-recorder
%{_datadir}/gstreamer-properties
%{_datadir}/icons/hicolor/*/*/*.*
%dir %{_datadir}/sounds/
%dir %{_datadir}/sounds/gnome/
%{_datadir}/sounds/gnome/default/

