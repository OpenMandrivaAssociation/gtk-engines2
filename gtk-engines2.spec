%define pkgname gtk-engines
%define pkgversion 2
%define lib_name %mklibname %{pkgname}%{pkgversion}

%define cleanice_version 2.4.0
%define xfce_version 2.4.1
%define wonderland_version 0.47
%define mist_version 0.5

%define _requires_exceptions pkgconfig\(.*\)

%define gtkbinaryver %(if $([ -x %{_bindir}/pkg-config ] && pkg-config --exists gtk+-2.0); then pkg-config --variable=gtk_binary_version gtk+-2.0; else echo 0; fi)

Name:			%{pkgname}%{pkgversion}
Summary:		Default GTK+ 2.0 theme engines
Version:		2.10.2
Release:		%mkrel 1
License:		GPL
Group:			System/Libraries
BuildRequires:		libglade2.0-devel
BuildRequires:		gtk+2-devel >= 2.6.0
BuildRequires:		perl-XML-Parser
Source0:		http://ftp.gnome.org/pub/GNOME/sources/gtk-engines/%{pkgname}-%{version}.tar.bz2
Source3:		http://prdownloads.sourceforge.net/elysium-project/gtk-engines-cleanice-%{cleanice_version}.tar.bz2
Source4:		http://www.xfce.org/archive/xfce-4.4.0/gtk-xfce-engine-%{xfce_version}.tar.bz2
Source5:		http://themes.freshmeat.net/redir/gtk2flat/31385/url_tgz/gtk2flat-default.tar.bz2
Source7:		Wonderland-%{wonderland_version}.tar.bz2
Url:			ftp://ftp.gnome.org/pub/GNOME/sources/gtk-engines/

BuildRoot:		%{_tmppath}/%{name}-%{version}-buildroot
Requires:		%{lib_name} >= %{version}
Conflicts:		ximian-artwork < 0.2.26-4mdk
Conflicts:		gnome-themes <= 2.8.2-2mdk
Conflicts:		gnome-themes-extras < 0.8.0-3mdk
Provides:		gtk-theme-clearlooks gtk-xfce-engine 
Obsoletes:		gtk-theme-clearlooks gtk-xfce-engine 

%description
These are the graphical engines for the various GTK+ toolkit themes.
Included themes are:

  - Notif
  - Redmond95
  - Pixmap
  - Metal (swing-like)
  - Many more


#--------------------------------------------------------------------

%package -n %{lib_name}
Summary:	Library files for %{name}
Group:		System/Libraries
Requires:	gtk+2.0 >= 2.9.0
Provides:	%lib_name = %version
Conflicts:      %name < 2.8.2

%description -n %{lib_name}
Library files for %{name}


%prep
%setup -q -n %{pkgname}-%{version} -a 3 -a 4 -a 5 -a 7

%build

%configure2_5x --enable-lua
%make

cd gtk-engines-cleanice-%{cleanice_version}/
%configure2_5x
%make
cd ..

cd gtk-xfce-engine-%{xfce_version}/
%configure2_5x
%make
cd ..

cd gtk-flat-theme-2.0/
%configure2_5x
%make
cd ..

cd Wonderland-%{wonderland_version}/
%define __libtoolize /bin/true
%configure2_5x
%make
cd ..

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std

cd gtk-engines-cleanice-%{cleanice_version}/
%makeinstall_std
cd ..

cd gtk-xfce-engine-%{xfce_version}/
%makeinstall_std
cd ..

cd gtk-flat-theme-2.0/
%makeinstall_std
cd ..

cd Wonderland-%{wonderland_version}/
%makeinstall_std
cd ..

#remove empty files
rm -f $RPM_BUILD_ROOT%{_datadir}/themes/*/ICON.png \
  $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/%{gtkbinaryver}/engines/*.la \
  $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/%{gtkbinaryver}/engines/*.a 

%find_lang %pkgname

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


#--------------------------------------------------------------------

%files -f %pkgname.lang
%defattr(-,root,root)
%doc COPYING README ChangeLog
%{_datadir}/themes/*
%_datadir/gtk-engines/

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/gtk-2.0/%{gtkbinaryver}/engines/*.so
%{_libdir}/pkgconfig/*
