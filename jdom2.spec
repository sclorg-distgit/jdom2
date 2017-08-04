%{?scl:%scl_package jdom2}
%{!?scl:%global pkg_name %{name}}

Name:          %{?scl_prefix}jdom2
Version:       2.0.6
Release:       7.2%{?dist}
Summary:       Java manipulation of XML made easy
License:       ASL 1.1 or BSD
URL:           http://www.jdom.org/
Source0:       https://github.com/hunterhacker/jdom/archive/JDOM-%{version}.tar.gz
# originally taken from http://repo1.maven.org/maven2/org/jdom/jdom-contrib/1.1.3/jdom-contrib-1.1.3.pom
Source1:       jdom-contrib-template.pom
Source2:       jdom-junit-template.pom
# Bnd tool configuration
Source3:       bnd.properties
# Use system libraries
# Disable gpg signatures
# Process contrib and junit pom files
Patch0:        jdom-2.0.5-build.patch

BuildRequires: %{?scl_prefix}javapackages-local
BuildRequires: %{?scl_prefix}ant
BuildRequires: %{?scl_prefix}ant-junit
BuildRequires: %{?scl_prefix}bea-stax-api
BuildRequires: %{?scl_prefix}isorelax
BuildRequires: %{?scl_prefix}jaxen
BuildRequires: %{?scl_prefix}xalan-j2
BuildRequires: %{?scl_prefix}xerces-j2
BuildRequires: %{?scl_prefix}xml-commons-apis
BuildRequires: %{?scl_prefix}log4j12
BuildRequires: %{?scl_prefix}objectweb-asm3
BuildRequires: %{?scl_prefix}aqute-bnd

BuildArch:     noarch

%description
JDOM is a Java-oriented object model which models XML documents.
It provides a Java-centric means of generating and manipulating
XML documents. While JDOM inter-operates well with existing
standards such as the Simple API for XML (SAX) and the Document
Object Model (DOM), it is not an abstraction layer or
enhancement to those APIs. Rather, it seeks to provide a robust,
light-weight means of reading and writing XML data without the
complex and memory-consumptive options that current API
offerings provide.

%package javadoc
Summary:       Javadoc for %{pkg_name}

%description javadoc
This package contains javadoc for %{pkg_name}.

%prep
%setup -q -n jdom-JDOM-%{version}
find . -name "*.class" -print -delete
find . -name "*.jar" -print -delete

%patch0 -p1

cp -p %{SOURCE1} maven/contrib.pom
cp -p %{SOURCE2} maven/junit.pom

sed -i 's/\r//' LICENSE.txt README.txt

# Unable to run coverage: use log4j12 but switch to log4j 2.x
sed -i.coverage "s|coverage, jars|jars|" build.xml

build-jar-repository lib xerces-j2 xml-commons-apis jaxen junit isorelax xalan-j2 xalan-j2-serializer

%build
ant -Dversion=%{version} -Dj2se.apidoc=%{_javadocdir}/java maven

# Make jar into an OSGi bundle
bnd wrap --output build/package/jdom-%{version}.bar --properties %{SOURCE3} \
         --version %{version} build/package/jdom-%{version}.jar
mv build/package/jdom-%{version}.bar build/package/jdom-%{version}.jar

%install
%mvn_artifact build/maven/core/%{pkg_name}-%{version}.pom build/package/jdom-%{version}.jar
%mvn_artifact build/maven/core/%{pkg_name}-%{version}-contrib.pom build/package/jdom-%{version}-contrib.jar
%mvn_artifact build/maven/core/%{pkg_name}-%{version}-junit.pom build/package/jdom-%{version}-junit.jar
%mvn_install -J build/apidocs

%files -f .mfiles
%doc CHANGES.txt COMMITTERS.txt README.txt TODO.txt
%license LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Thu Jun 22 2017 Michael Simacek <msimacek@redhat.com> - 2.0.6-7.2
- Mass rebuild 2017-06-22

* Wed Jun 21 2017 Java Maintainers <java-maint@redhat.com> - 2.0.6-7.1
- Automated package import and SCL-ization

* Wed May 31 2017 Michael Simacek <msimacek@redhat.com> - 2.0.6-7
- Avoid hardcoded jar paths

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Apr 14 2016 Mat Booth <mat.booth@redhat.com> - 2.0.6-6
- Add OSGi metadata to main jar
- Fix file listed twice warning

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 24 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.6-3
- Remove unneeded BR on cobertura

* Fri Feb 06 2015 gil cattaneo <puntogil@libero.it> 2.0.6-2
- introduce license macro

* Tue Oct 21 2014 gil cattaneo <puntogil@libero.it> 2.0.6-1
- update to 2.0.6 (rhbz#1118627)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.0.5-3
- Use Requires: java-headless rebuild (#1067528)

* Thu Nov 14 2013 gil cattaneo <puntogil@libero.it> 2.0.5-2
- use objectweb-asm3

* Thu Sep 12 2013 gil cattaneo <puntogil@libero.it> 2.0.5-1
- initial rpm
