//============================================================================
/// \file   MetroStylePlugin.cpp
/// \author Softwareentwickler01
/// \date   10.08.2012
/// \brief  Implementation of CMetroStylePlugin
//============================================================================

//============================================================================
//                                   INCLUDES
//============================================================================
#include "MetroStylePlugin.h"

#include <QtCore>
#include <QPixmap>
#include <QtCore/qglobal.h>
#include <QApplication>
#include <QPalette>
#include <QProxyStyle>
#include <QPainter>
#include <QToolTip>
#include <QStyleFactory>

#include <qtlabb/core/stylemanager/StyleManager.h>
#include <iostream>

extern int QT_MANGLE_NAMESPACE(qInitResources_metro)();
extern int QT_MANGLE_NAMESPACE(qInitResources_plugin)();

namespace MetroStyle
{
/**
 * Metro specific implementation of some style functions
 * This proxy style provides SVG message box icons until proper support for
 * high DPI icons for Windows 10 is implemented in Qt
 */
class CMetroProxyStyle : public QProxyStyle
{
public:
	QtLabb::Core::CStyleManager* m_StyleManager = nullptr;

    /**
     * Create proxy style for fusion style
     */
    CMetroProxyStyle() : QProxyStyle(QStyleFactory::create("Fusion")) {}

	/**
	 * Returns metro specific icons for message box
	 */
	virtual QIcon standardIcon(StandardPixmap IconID,
		const QStyleOption* option, const QWidget * widget) const
	{
		switch (IconID)
		{
		case QStyle::SP_MessageBoxInformation:
		{
			static const QIcon Icon("icon:/normal/information.svg");
			return Icon;
		}
		break;

		case QStyle::SP_MessageBoxWarning:
		{
			static const QIcon Icon("icon:/normal/warning.svg");
			return Icon;
		}

		case QStyle::SP_MessageBoxCritical:
		{
			static const QIcon Icon("icon:/normal/error.svg");
			return Icon;
		}

		case QStyle::SP_MessageBoxQuestion:
		{
			static const QIcon Icon("icon:/normal/question.svg");
			return Icon;
		}

		case QStyle::SP_DialogCancelButton:
		{
			static const QIcon Icon("icon:/normal/cancel.svg");
			return Icon;
		}


		case QStyle::SP_DialogOkButton:
		case QStyle::SP_DialogApplyButton:
		case QStyle::SP_DialogYesButton:
		{
			static const QIcon Icon("icon:/normal/check2.svg");
			return Icon;
		}

		case QStyle::SP_DialogDiscardButton:
		case QStyle::SP_DialogCloseButton:
		case QStyle::SP_DialogNoButton:
		{
			static const QIcon Icon("icon:/normal/delete2.svg");
			return Icon;
		}

		case QStyle::SP_DialogSaveButton:
		{
			static const QIcon Icon("icon:/normal/floppy_disk.svg");
			return Icon;
		}

		case QStyle::SP_DialogResetButton:
		{
			static const QIcon Icon("icon:/normal/reset.svg");
			return Icon;
		}

		case QStyle::SP_DialogHelpButton:
		{
			static const QIcon Icon("icon:/normal/help.svg");
			return Icon;
		}


		case QStyle::SP_DirIcon:
		{
			static const QIcon Icon("icon:/normal/folder.svg");
			return Icon;
		}

		case QStyle::SP_DialogOpenButton:
		case QStyle::SP_DirOpenIcon:
		{
			static const QIcon Icon("icon:/normal/folder_open.svg");
			return Icon;
		}

		case QStyle::SP_FileIcon:
		{
			static const QIcon Icon("icon:/normal/document.svg");
			return Icon;
		}

		case QStyle::SP_LineEditClearButton:
		{
			static const QIcon Icon = m_StyleManager->loadThemeAwareSvgIcon("icon:/normal/lineedit_delete_button.svg");
			return Icon;
		}

		default:
			return QProxyStyle::standardIcon(IconID, option, widget);
		}

		return QProxyStyle::standardIcon(IconID, option, widget);
	}


	QPixmap generatedIconPixmap(QIcon::Mode iconMode, const QPixmap &pixmap, const QStyleOption *opt) const override
	{
		return QProxyStyle::generatedIconPixmap(iconMode, pixmap, opt);
#if 0
        if (iconMode != QIcon::Mode::Disabled)        {
            return QProxyStyle::generatedIconPixmap(iconMode, pixmap, opt);
        }

        QImage im = pixmap.toImage();
        for (int y = 0; y < im.height(); ++y)
        {
            QRgb* scanLine = (QRgb*)im.scanLine(y);
            for (int x = 0; x < im.width(); ++x)
            {
                QRgb pixel = *scanLine;
                uint ci = uint(qGray(pixel));
                *scanLine = qRgba(ci, ci, ci, qAlpha(pixel) / 3);
                ++scanLine;
            }
        }

        QImage image(pixmap.size(), QImage::Format_ARGB32_Premultiplied); //Image with given size and format.
		image.fill(Qt::transparent); //fills with transparent
		QPainter p(&image);
		p.setOpacity(0.5); // set opacity from 0.0 to 1.0, where 0.0 is fully transparent and 1.0 is fully opaque.
		p.drawImage(0, 0, im);
		p.end();
		return QPixmap::fromImage(image);
#endif
	}

	virtual int pixelMetric(QStyle::PixelMetric metric, const QStyleOption *option = nullptr, const QWidget *widget = nullptr) const override
	{
		// The fusion style returns a message box icon size of 48 pixels - that does not look good on windows
		if (QStyle::PM_MessageBoxIconSize == metric)
		{
			return 32;
		}
		else
		{
			return QProxyStyle::pixelMetric(metric, option, widget);
		}
	}
};


//============================================================================
CMetroStylePlugin::CMetroStylePlugin()
{
	QT_MANGLE_NAMESPACE(qInitResources_plugin)();
	m_Thumbnail = QPixmap(":/metro/images/style_preview.png");
}


//============================================================================
const QString& CMetroStylePlugin::styleName() const
{
	static const QString StyleName = "Metro Style";
	return StyleName;
}

//============================================================================
const QPixmap& CMetroStylePlugin::styleThumbnail() const
{
	return m_Thumbnail;
}

//============================================================================
void CMetroStylePlugin::load(QtLabb::Core::CStyleManager* StyleManager)
{
	QT_MANGLE_NAMESPACE(qInitResources_metro)();
	m_StyleManager = StyleManager;
	auto ProxyStyle = new CMetroProxyStyle();
	ProxyStyle->m_StyleManager = StyleManager;
    qApp->setStyle(ProxyStyle);

    // Invalidate the palette to work around QTBUG-123570
    QToolTip::setPalette(QPalette());
}
}  // namespace MetroStyle


#if QT_VERSION < QT_VERSION_CHECK(5,0,0)
Q_EXPORT_PLUGIN2(MetroStyle, MetroStyle::CMetroStylePlugin);
#endif
//---------------------------------------------------------------------------
// EOF MetroStylePlugin.cpp
