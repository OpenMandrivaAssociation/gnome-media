%define lib_name %mklibname gnome-media %{lib_major}
%define develname %mklibname -d gnome-media
%define lib_major 0
%define req_gail_version                       0.13
%define req_gstreamer_version		0.10

Summary:	GNOME media programs
Name:		gnome-media
Version: 2.32.0
Release: %mkrel 3
License:	GPLv2+ and GFDL+
Group:		Graphical desktop/GNOME
BuildRequires:	ncurses-devel scrollkeeper sendmail-command
BuildRequires: gail-devel >= %{req_gail_version}
BuildRequires: libgstreamer-plugins-base-devel >= %{req_gstreamer_version}
BuildRequires: gstreamer0.10-plugins-base
BuildRequires:   gstreamer0.10-plugins-good
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
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
Patch0: gnome-media-2.29.91-format-string.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
URL:		http://www.gnome.org/
Requires:   gstreamer0.10-plugins-good
Requires:   gstreamer0.10-plugins-base
Suggests:   gstreamer0.10-flac
Suggests:   gstreamer0.10-speex
Obsoletes:	grecord
Provides:	grecord
Requires(post):	scrollkeeper >= 0.3
Requires(postun):	scrollkeeper >= 0.3
Requires(post):	GConf2 >= 2.3.3
Requires(preun):	GConf2 >= 2.3.3

%description
This package contains a few media utilities for the GNOME desktop,
including a sound recorder and an audio mixer.

%package -n %{lib_name}
Summary:	%{summary}
Group:		System/Libraries
Requires:	%{name} >= %{version}
Obsoletes:	%mklibname cddb-slave 2 0

%description -n %{lib_name}
libraries for running GNOME media.

%package -n %develname
Summary:	Static libraries, include files for GNOME media
Group:		Development/GNOME and GTK+
Provides:	libcddb-slave2-devel = %{version}-%{release}
Provides:	%name-devel = %version-%release
Requires:	%{lib_name} = %{version}-%{release}
Obsoletes: 	%mklibname -d cddb-slave 2 0
Obsoletes: 	%mklibname -d cddb-slave 2

%description -n %develname
Panel libraries and header files for GNOME media.



%prep
%setup -q 
%apply_patches

%build

%configure2_5x  --disable-static

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
for omf in %buildroot%_datadir/omf/*/{*-??.omf,};do
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed s!%buildroot!!)" >> %name-2.0.lang
done

%clean
rm -rf %{buildroot}

%post
%define schemas gnome-sound-recorder gnome-audio-profiles

%preun
%preun_uninstall_gconf_schemas %schemas

%files -f  %{name}-2.0.lang
%defattr(-, root, root)
%doc AUTHORS NEWS README
%_sysconfdir/xdg/autostart/gnome-volume-control-applet.desktop
%{_sysconfdir}/gconf/schemas/gnome-sound-recorder.schemas
%{_sysconfdir}/gconf/schemas/gnome-audio-profiles.schemas
%{_bindir}/*
%_libdir/glade3/modules/libgnome-media-profiles.la
%_libdir/glade3/modules/libgnome-media-profiles.so
%_datadir/glade3/catalogs/gnome-media-profiles.xml
%{_datadir}/applications/gnome-sound-recorder.desktop
%{_datadir}/applications/gnome-volume-control.desktop
%{_datadir}/applications/gstreamer-properties.desktop
%{_datadir}/gnome-media
%{_datadir}/gnome-sound-recorder
%{_datadir}/gstreamer-properties
%_datadir/icons/hicolor/*/*/*.*
%dir %_datadir/sounds/
%dir %_datadir/sounds/gnome/
%_datadir/sounds/gnome/default/

%files -n  %{lib_name}
%defattr(-, root, root)
%{_libdir}/libgnome-media-profiles.so.%{lib_major}*

%files -n  %develname
%defattr(-, root, root)
%{_libdir}/*.so
%attr(644,root,root) %{_libdir}/*.la
%{_libdir}/pkgconfig/gnome-media-profiles.pc
%{_includedir}/*
