%define url_ver %(echo %{version} | cut -d. -f1,2)
%define	gstapi	0.10

Summary:	GNOME media programs
Name:		gnome-media
Version:	3.4.0
Release:	6
License:	GPLv2+ and GFDL+
Group:		Graphical desktop/GNOME
Url:		http://www.gnome.org/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-media/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires:	desktop-file-utils
BuildRequires:	gnome-doc-utils
BuildRequires:	intltool >= 0.35
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gnome-keybindings)
BuildRequires:	pkgconfig(gstreamer-%{gstapi})
BuildRequires:	pkgconfig(gstreamer-plugins-base-%{gstapi})
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libcanberra-gtk3)
BuildRequires:	pkgconfig(libgnome-media-profiles-3.0)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libxml-2.0)

Requires:	gstreamer%{gstapi}-plugins-good
Requires:	gstreamer%{gstapi}-plugins-base
Suggests:	gstreamer%{gstapi}-flac
Suggests:	gstreamer%{gstapi}-speex
Requires(post,preun):	GConf2

%description
This package contains a few media utilities for the GNOME desktop,
including a sound recorder and an audio mixer.

%prep
%setup -q 
%apply_patches

%build
%configure2_5x \
	--disable-static \
	--disable-scrollkeeper

%make

%install
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

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
%{_iconsdir}/hicolor/*/*/*.*
%dir %{_datadir}/sounds/
%dir %{_datadir}/sounds/gnome/
%{_datadir}/sounds/gnome/default/

