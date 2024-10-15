# Use the official Bun image
FROM oven/bun:1 AS base
WORKDIR /usr/src/app

# Install Ionic CLI globally
RUN bun add -g @ionic/cli

# Install dependencies into temp directory
FROM base AS install

# Create temp directories for dev and prod
RUN mkdir -p /temp/dev /temp/prod

# Copy package files to temp directories and install dependencies
COPY frontend/package.json frontend/bun.lockb /temp/dev/
RUN cd /temp/dev && bun install --frozen-lockfile

# Install with --production (exclude devDependencies)
COPY frontend/package.json frontend/bun.lockb /temp/prod/
RUN cd /temp/prod && bun install --frozen-lockfile --production

# Copy node_modules from the temp directory and the frontend files
FROM base AS prerelease
COPY --from=install /temp/dev/node_modules node_modules
COPY frontend ./

# [optional] Build the Ionic app
RUN bun run build

# Final stage: Production image
FROM base AS release
COPY --from=install /temp/prod/node_modules node_modules
COPY --from=prerelease /usr/src/app/www ./www  # Copy built app files

# Expose the desired port (default is 3000)
EXPOSE 3000/tcp

# Run the app
ENTRYPOINT ["serve", "-s", "www", "-l", "3000"]
