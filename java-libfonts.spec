#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc

%define		srcname		libfonts
%include	/usr/lib/rpm/macros.java
Summary:	TrueType Font Layouting
Name:		java-%{srcname}
Version:	1.1.3
Release:	0.1
License:	LGPL v2+
Group:		Libraries/Java
Source0:	http://downloads.sourceforge.net/jfreereport/%{srcname}-%{version}.zip
# Source0-md5:	c7798a15a7409237dc48fe541d37cbf4
URL:		http://reporting.pentaho.org/
BuildRequires:	ant
BuildRequires:	ant-contrib
BuildRequires:	ant-nodeps
BuildRequires:	itext
BuildRequires:	java-libloader >= 1.1.3
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpmbuild(macros) >= 1.553
Requires:	itext
Requires:	java
Requires:	jpackage-utils
Requires:	libloader >= 1.1.3
BuildArch:	noarch
Patch0:		build.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibFonts is a library developed to support advanced layouting in
JFreeReport. This library allows to read TrueType-Font files to
extract layouting specific informations.

%package javadoc
Summary:	Javadoc for LibFonts
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
Requires:	jpackage-utils

%description javadoc
Javadoc for LibFonts.

%prep
%setup -qc
%patch0 -p1

find -name "*.jar" | xargs rm -v

%undos README.txt licence-LGPL.txt ChangeLog.txt

install -d lib
ln -s %{_javadir}/ant lib/ant-contrib

%build
build-jar-repository -s -p lib libbase commons-logging-api libloader itext
%ant jar %{?with_javadoc:javadoc}

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -a dist/%{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a bin/javadoc/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc licence-LGPL.txt README.txt ChangeLog.txt
%{_javadir}/%{srcname}.jar
%{_javadir}/%{srcname}-%{version}.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif

BuildRequires:  jpackage-utils
BuildRequires:  rpmbuild(macros) >= 1.300
