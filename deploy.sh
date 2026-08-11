#!/usr/bin/env bash
# ============================================================
# Course Hub deployer
# Syncs this whole folder (all course subfolders) to one S3
# bucket configured for public static-website hosting.
#
# Usage:
#   ./deploy.sh            # ensure bucket + sync everything
#   ./deploy.sh --dry-run  # show what would change, upload nothing
#
# Add a new course later: drop its folder here (with its own
# index.html), add a card to index.html, then run ./deploy.sh.
# ============================================================
set -euo pipefail
cd "$(dirname "$0")"

# --- load config ---
# shellcheck source=deploy.config
source ./deploy.config
: "${AWS_PROFILE:?}"; : "${AWS_REGION:?}"; : "${BUCKET:?}"
AWS="aws --profile ${AWS_PROFILE} --region ${AWS_REGION}"
DRY=""
[ "${1:-}" = "--dry-run" ] && DRY="--dryrun"

echo ">> Profile ${AWS_PROFILE} | Region ${AWS_REGION} | Bucket ${BUCKET}"

# --- ensure bucket exists ---
if ! $AWS s3api head-bucket --bucket "$BUCKET" 2>/dev/null; then
  echo ">> Creating bucket ${BUCKET} ..."
  if [ "$AWS_REGION" = "us-east-1" ]; then
    $AWS s3api create-bucket --bucket "$BUCKET"
  else
    $AWS s3api create-bucket --bucket "$BUCKET" \
      --create-bucket-configuration LocationConstraint="$AWS_REGION"
  fi

  echo ">> Disabling Block Public Access ..."
  $AWS s3api put-public-access-block --bucket "$BUCKET" \
    --public-access-block-configuration \
    BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false

  echo ">> Applying public-read bucket policy ..."
  $AWS s3api put-bucket-policy --bucket "$BUCKET" --policy "{
    \"Version\": \"2012-10-17\",
    \"Statement\": [{
      \"Sid\": \"PublicReadForCourses\",
      \"Effect\": \"Allow\",
      \"Principal\": \"*\",
      \"Action\": \"s3:GetObject\",
      \"Resource\": \"arn:aws:s3:::${BUCKET}/*\"
    }]
  }"

  echo ">> Enabling static website hosting ..."
  $AWS s3 website "s3://${BUCKET}" --index-document index.html --error-document index.html
fi

# --- sync (exclude non-site files) ---
echo ">> Syncing hub -> s3://${BUCKET} ..."
$AWS s3 sync . "s3://${BUCKET}" $DRY --delete \
  --exclude "*.md" \
  --exclude ".DS_Store" \
  --exclude ".git/*" \
  --exclude "deploy.sh" \
  --exclude "deploy.config" \
  --exclude "*/learning-records/*"

URL="http://${BUCKET}.s3-website.${AWS_REGION}.amazonaws.com/"
echo ""
echo ">> Done. Course Hub is live at:"
echo "   ${URL}"
