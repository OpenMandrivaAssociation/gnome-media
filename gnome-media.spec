%define major 0
%define libname %mklibname gnome-media %{major}
%define develname %mklibname -d gnome-media

Summary:	GNOME media programs
Name:		gnome-media
Version:	2.32.0
Release:	4
License:	GPLv2+ and GFDL+
Group:		Graphical desktop/GNOME
URL:		http://www.gnome.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
Patch0: gnome-media-2.29.91-format-string.patch

BuildRequires: ncurses-devel
BuildRequires: sendmail-command
BuildRequires: gail-devel 
BuildRequires: libgstreamer-plugins-base-devel 
BuildRequires: gstreamer0.10-plugins-base
BuildRequires: gstreamer0.10-plugins-good
BuildRequires: libGConf2-devel
BuildRequires: gtk+2-devel
BuildRequires: glade3-devel
BuildRequires: libgnome-window-settings-devel
BuildRequires: libxrender-devel
BuildRequires: libcanberra-gtk-devel
BuildRequires: pulseaudio-devel
BuildRequires: unique-devel
BuildRequires: gnome-doc-utils
BuildRequires: intltool >= 0.35
BuildRequires: desktop-file-utils

Requires:   gstreamer0.10-plugins-good
Requires:   gstreamer0.10-plugins-base
Suggests:   gstreamer0.10-flac
Suggests:   gstreamer0.10-speex
Obsoletes:	grecord
Provides:	grecord
Requires(post):	GConf2 >= 2.3.3
Requires(preun):	GConf2 >= 2.3.3

%description
This package contains a few media utilities for the GNOME desktop,
including a sound recorder and an audio mixer.

%package -n %{libname}
Summary:	%{summary}
Group:		System/Libraries
Obsoletes:	%mklibname cddb-slave 2 0

%description -n %{libname}
libraries for running GNOME media.

%package -n %{develname}
Summary:	Development libraries, include files for GNOME media
Group:		Development/GNOME and GTK+
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Obsoletes: 	%mklibname -d cddb-slave 2 0
Obsoletes: 	%mklibname -d cddb-slave 2

%description -n %{develname}
Panel libraries and header files for GNOME media.

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

desktop-file-install --vendor="" \
  --add-category="DesktopSettings" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/gstreamer-properties.desktop

desktop-file-install --vendor="" \
  --add-category="X-MandrivaLinux-CrossDesktop" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/gnome-sound-recorder.desktop

%find_lang %{name}-2.0 --with-gnome --all-name
for omf in %{buildroot}%{_datadir}/omf/*/{*-??.omf,};do
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed s!%{buildroot}!!)" >> %{name}-2.0.lang
done

%post
%define schemas gnome-sound-recorder gnome-audio-profiles

%preun
%preun_uninstall_gconf_schemas %schemas

%files -f  %{name}-2.0.lang
%doc AUTHORS NEWS README
%{_sysconfdir}/xdg/autostart/gnome-volume-control-applet.desktop
%{_sysconfdir}/gconf/schemas/gnome-sound-recorder.schemas
%{_sysconfdir}/gconf/schemas/gnome-audio-profiles.schemas
%{_bindir}/*
%{_libdir}/glade3/modules/libgnome-media-profiles.la
%{_libdir}/glade3/modules/libgnome-media-profiles.so
%{_datadir}/glade3/catalogs/gnome-media-profiles.xml
%{_datadir}/applications/gnome-sound-recorder.desktop
%{_datadir}/applications/gnome-volume-control.desktop
%{_datadir}/applications/gstreamer-properties.desktop
%{_datadir}/gnome-media
%{_datadir}/gnome-sound-recorder
%{_datadir}/gstreamer-properties
%{_datadir}/icons/hicolor/*/*/*.*
%dir %{_datadir}/sounds/
%dir %{_datadir}/sounds/gnome/
%{_datadir}/sounds/gnome/default/

%files -n  %{libname}
%{_libdir}/libgnome-media-profiles.so.%{major}*

%files -n  %{develname}
%{_libdir}/*.so
%{_libdir}/pkgconfig/gnome-media-profiles.pc
%dir %{_includedir}/gnome-media
%dir %{_includedir}/gnome-media/profiles
%{_includedir}/gnome-media/profiles/*

