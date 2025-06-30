include(../../qtlabblibrary.pri)
include(../../core/core.pri)

TEMPLATE = lib
TARGET = $$uslQtLibraryTarget(qtlabb_style_metro, d)

DEPENDPATH += $$PWD

HEADERS += MetroStylePlugin.h

SOURCES += MetroStylePlugin.cpp

RESOURCES += metro.qrc \
    plugin.qrc

