#
# Conditional build:
%bcond_without	tests	# unit tests

%define	module gunicorn
Summary:	Python WSGI application server
Summary(pl.UTF-8):	Pythonowy serwer aplikacji WSGI
Name:		python3-%{module}
Version:	23.0.0
Release:	1
License:	MIT
Group:		Daemons
#Source0Download: https://pypi.org/simple/gunicorn/
Source0:	https://files.pythonhosted.org/packages/source/g/gunicorn/%{module}-%{version}.tar.gz
# Source0-md5:	18b666db62a890579170639961c5b064
# distro-specific, not upstreamable
Patch100:	%{name}-dev-log.patch
URL:		https://gunicorn.org/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools >= 1:61.2
%if %{with tests}
BuildRequires:	python3-coverage >= 4.0
BuildRequires:	python3-eventlet >= 0.24.1
BuildRequires:	python3-gevent >= 1.4.0
BuildRequires:	python3-packaging
%if "%{py3_ver}" == "3.7"
BuildRequires:	python3-importlib_metadata
%endif
BuildRequires:	python3-pytest >= 7.2.0
BuildRequires:	python3-pytest-cov >= 2.5.1
BuildRequires:	python3-tornado >= 0.2
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	sphinx-pdg-3
BuildRequires:	python3-docutils
BuildRequires:	python3-sphinx_rtd_theme
%endif
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gunicorn ("Green Unicorn") is a Python WSGI HTTP server for UNIX. It
uses the pre-fork worker model, ported from Ruby's Unicorn project. It
supports WSGI, Django, and Paster applications.

%description -l pl.UTF-8
Gunicorn ("Green Unicorn" - zielony jednorożec) to pythonowy serwer
HTTP WSGI dla systemów uniksowych. Wykorzystuje model pre-fork,
przeniesiony z projektu Unicorn napisanego w języku Ruby. Obsługuje
aplikacje WSGI, Django i Paster.

%prep
%setup -q -n %{module}-%{version}
%patch -P 100 -p1

%build
%py3_build_pyproject

%if %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_cov.plugin" \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE NOTICE README.rst THANKS
%attr(755,root,root) %{_bindir}/gunicorn
%{py3_sitescriptdir}/gunicorn
%{py3_sitescriptdir}/gunicorn-%{version}.dist-info
