#!/bin/bash
# Restructure Estate Monitor App

APP_DIR="./app"

echo "📦 Creating folder structure..."
mkdir -p $APP_DIR/{api,core,database,models,schemas,services,utils,ws,static/{css,js,images,media},templates/{auth,dashboard,tenant,owner,admin,pdf,subscription},billing,dependencies}

echo "📂 Moving API routers..."
mv $APP_DIR/api/auth $APP_DIR/api/
mv $APP_DIR/api/dashboard $APP_DIR/api/
mv $APP_DIR/api/owner $APP_DIR/api/
mv $APP_DIR/api/payments $APP_DIR/api/
mv $APP_DIR/api/properties $APP_DIR/api/
mv $APP_DIR/api/profile $APP_DIR/api/
mv $APP_DIR/api/tenant $APP_DIR/api/
mv $APP_DIR/api/admin $APP_DIR/api/
mv $APP_DIR/api/ads $APP_DIR/api/

echo "📂 Moving core files..."
mv $APP_DIR/core/*.py $APP_DIR/core/

echo "📂 Moving database files..."
mv $APP_DIR/database/*.py $APP_DIR/database/

echo "📂 Moving models..."
mv $APP_DIR/models/*.py $APP_DIR/models/

echo "📂 Moving schemas..."
mv $APP_DIR/schemas/*.py $APP_DIR/schemas/

echo "📂 Moving services..."
mv $APP_DIR/services/*.py $APP_DIR/services/

echo "📂 Moving utils..."
mv $APP_DIR/utils/*.py $APP_DIR/utils/

echo "📂 Moving WebSockets..."
mv $APP_DIR/ws/*.py $APP_DIR/ws/

echo "📂 Moving static files..."
mv $APP_DIR/static/css/*.css $APP_DIR/static/css/
mv $APP_DIR/static/js/*.js $APP_DIR/static/js/
mv $APP_DIR/static/images/* $APP_DIR/static/images/
mv $APP_DIR/static/media/* $APP_DIR/static/media/

echo "📂 Moving templates..."
mv $APP_DIR/templates/auth/* $APP_DIR/templates/auth/
mv $APP_DIR/templates/dashboard/* $APP_DIR/templates/dashboard/
mv $APP_DIR/templates/tenant/* $APP_DIR/templates/tenant/
mv $APP_DIR/templates/owner/* $APP_DIR/templates/owner/
mv $APP_DIR/templates/admin/* $APP_DIR/templates/admin/
mv $APP_DIR/templates/pdf/* $APP_DIR/templates/pdf/
mv $APP_DIR/templates/subscription/* $APP_DIR/templates/subscription/

echo "✅ Restructure complete!"
