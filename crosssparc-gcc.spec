Summary:	Cross SPARC GNU binary utility development utilities - gcc
Summary(es):	Utilitarios para desarrollo de binarios de la GNU - SPARC gcc
Summary(fr):	Utilitaires de développement binaire de GNU - SPARC gcc
Summary(pl):	Skro¶ne narzêdzia programistyczne GNU dla SPARC - gcc
Summary(pt_BR):	Utilitários para desenvolvimento de binários da GNU - SPARC gcc
Summary(tr):	GNU geliþtirme araçlarý - SPARC gcc
Name:		crosssparc-gcc
Version:	3.4.3
Release:	2
Epoch:		1
License:	GPL
Group:		Development/Languages
Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{version}/gcc-%{version}.tar.bz2
# Source0-md5:	e744b30c834360fccac41eb7269a3011
URL:		http://gcc.gnu.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	crosssparc-binutils
BuildRequires:	flex
BuildRequires:	/bin/bash
Requires:	crosssparc-binutils
Requires:	gcc-dirs
ExcludeArch:	sparc sparcv9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		sparc-pld-linux
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_libdir}/gcc/%{target}
%define		gcclib		%{gccarch}/%{version}

%define		_noautostrip	.*/libgc.*\\.a

%description
This package contains a cross-gcc which allows the creation of
binaries to be run on SPARC Linux on other machines.

%description -l de
Dieses Paket enthält einen Cross-gcc, der es erlaubt, auf einem
anderem Rechner Code für SPARC Linux zu generieren.

%description -l pl
Ten pakiet zawiera skro¶ny gcc pozwalaj±cy na robienie na innych
maszynach binariów do uruchamiania na Linuksie SPARC.

%prep
%setup -q -n gcc-%{version}

%build
cp -f /usr/share/automake/config.* .
rm -rf obj-%{target}
install -d obj-%{target}
cd obj-%{target}

CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcflags}" \
TEXCONFIG=false \
../configure \
	--prefix=%{_prefix} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libdir} \
	--disable-shared \
	--disable-threads \
	--enable-languages="c" \
	--enable-c99 \
	--enable-long-long \
	--with-gnu-as \
	--with-gnu-ld \
	--with-system-zlib \
	--with-multilib \
	--without-headers \
	--without-x \
	--target=%{target} \
	--host=%{_target_platform} \
	--build=%{_target_platform}

%{__make} all-gcc

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C obj-%{target} install-gcc \
	DESTDIR=$RPM_BUILD_ROOT

# don't want this here
rm -f $RPM_BUILD_ROOT%{_libdir}/libiberty.a

%if 0%{!?debug:1}
%{target}-strip -g -R.note -R.comment $RPM_BUILD_ROOT%{gcclib}/libgcc.a
%{target}-strip -g -R.note -R.comment $RPM_BUILD_ROOT%{gcclib}/libgcov.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-cpp
%attr(755,root,root) %{_bindir}/%{target}-gcc
%dir %{gccarch}
%dir %{gcclib}
%attr(755,root,root) %{gcclib}/cc1
%attr(755,root,root) %{gcclib}/collect2
%{gcclib}/crt*.o
%{gcclib}/libgcc.a
%{gcclib}/specs*
%dir %{gcclib}/include
%{gcclib}/include/*.h
%{_mandir}/man1/%{target}-cpp.1*
%{_mandir}/man1/%{target}-gcc.1*
