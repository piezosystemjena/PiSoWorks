#ifndef MetroStylePluginH
#define MetroStylePluginH
//============================================================================
/// \file   MetroStylePlugin.h
/// \author Softwareentwickler01
/// \date   10.08.2012
/// \brief  Declaration of CMetroStylePlugin
//============================================================================

//============================================================================
//                                   INCLUDES
//============================================================================
#include <qtlabb/core/stylemanager/IStylePlugin.h>
#include <QPixmap>

namespace MetroStyle
{

/**
 * IStylePlugin implementation for drak style
 */
class CMetroStylePlugin : public QtLabb::Core::IStylePlugin
{
	Q_OBJECT
	Q_INTERFACES(QtLabb::Core::IStylePlugin)
#if QT_VERSION >= QT_VERSION_CHECK(5,0,0)
    Q_PLUGIN_METADATA(IID "cetoni.qtlabb.core.CMetroStylePlugin")
#endif

private:
	QPixmap m_Thumbnail;
	QtLabb::Core::CStyleManager* m_StyleManager;

public:
	/**
	 * Default constructor
	 */
	CMetroStylePlugin();

public:
	// IStylePlugin implementation -------------------------------------
	virtual const QString& styleName() const;
	virtual const QPixmap& styleThumbnail() const;
	virtual void load(QtLabb::Core::CStyleManager* StyleManager);
};
// class CMetroStylePlugin
}// namespace dark


//---------------------------------------------------------------------------
#endif // MetroStylePluginH
